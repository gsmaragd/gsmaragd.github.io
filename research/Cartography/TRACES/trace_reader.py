#!/usr/bin/env python

import sys
import os
import optparse
import traceback
import bz2

try:
    import dns.message
    import dns.rdatatype
    import dns.version
except ImportError:
    print >>sys.stderr, "ERROR: You need to install dnspython."
    print >>sys.stderr, "  Use 'aptitude install python-dnspython' on Debian or Ubuntu based machines."
    sys.exit(1)

if dns.version.MAJOR == 1 and dns.version.MINOR == 7:
    print >>sys.stderr, "ERROR: The version of dnspython is %s. This version" % dns.version.version
    print >>sys.stderr, "       is known to be broken and can be very slow."
    print >>sys.stderr, "       Please use 1.6.x or 1.8.x instead."
    sys.exit(1)


class TraceExtractor (object):

    def __init__ (self, filename, prefix="", postfix=".txt"):
        fname = prefix + filename + postfix
        self.outputfile = open (fname, "w")

    def close (self):
        self.outputfile.close()

    def dump_query (self, ts, params, body):
            server, domainname, retrycount, success, delay = params.split(" ", 7)

            m = dns.message.from_text(body)
            a = m.answer

            ips = [ rr.address for rrset in a if rrset.rdtype == dns.rdatatype.A for rr in rrset  ]

            for rrset in a:
                if rrset.rdtype == dns.rdatatype.A:
                    for rr in rrset:
                        print >>self.outputfile, "answer", ts, server, domainname, rrset.name.to_text(), \
                              rrset.ttl, dns.rdataclass.to_text(rrset.rdclass), "A", rr.address


    def dump_failed (self, ts, params, body):
        assert body == ""
        server, domainname, reason = params.split(" ", 2)
        print >>self.outputfile, "failed", ts, server, domainname, reason


    def dump_resolver (self, ts, params, body):
        assert body == ""
        nameserver, server_ip, ptr_to_resolver = params.split (" ", 2)
        print >>self.outputfile, "resolver", ts, nameserver, server_ip, ptr_to_resolver


    def dump_host (self, ts, params, body):
        assert body == ""
        host_ip = params
        print >>self.outputfile, "host", host_ip


    def dump_messages (self, status, ts, params, body):

        if status == "Query:":
            self.dump_query(ts, params, body)

        elif status == "Failed:":
            self.dump_failed (ts, params, body)

        elif status == "Resolver:":
            self.dump_resolver(ts, params, body)

        elif status == "Host:":
            self.dump_host(ts, params, body)


def parseopts (argv):
    parser = optparse.OptionParser (usage = "trace_reader.py [options] <tracefile> [ <tracefile> [ ... ] ]")
    parser.add_option ("-P", "--prefix", action="store", default = "",
                       help="prefix output files with PREFIX")

    return parser.parse_args (argv)

########### MAIN ###########

if __name__ == "__main__":
    opts, args = parseopts (sys.argv)

    for filename in args[1:]:
        print "="*80
        print "Working on", filename

        extractor = TraceExtractor (filename, prefix = opts.prefix)
        handler = extractor.dump_messages

        try:
            f = bz2.BZ2File (filename)
            for line in f:
                status, bodylen, ts, rest = line.split (" ", 3)
                body = "".join (f.next() for i in range(int(bodylen)))
                handler (status, ts, rest.strip(), body)

        except KeyboardInterrupt:
            raise

        except:
            print >>sys.stderr, "line: '%s'" % line.rstrip("\n")
            traceback.print_exc()

        finally:
            extractor.close()
