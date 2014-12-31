#!/usr/bin/env python 

import sys, twitter, os, time, random, datetime, serial
from time import strftime, sleep

class Xmas(object):

    def __init__(self):
        self.LATESTFILE = 'xmaslastest.txt'
        self.LOGFILE = 'xmaslog.txt'
        # Add your twitter dev keys here
        # Use this tutorial if you need help https://facelesstech.wordpress.com/2014/01/01/tweeting-from-python/
        self.api = twitter.Api(consumer_key='',
                  consumer_secret='',
                  access_token_key='',
                  access_token_secret='') 

    def xmas_ascii(self):
        print"""
                                    .!,            .!,
                                   ~ 6 ~          ~ 6 ~
                              .    ' i `  .-^-.   ' i `
                            _.|,_   | |  / .-. \   | |
                             '|`   .|_|.| (-` ) | .|_|.
                             / \ ___)_(_|__`-'__|__)_(______
                            /`,o\)_______________________o_(
                           /_* ~_\[___]___[___]___[___[_[\`-.
                           / o .'\[_]___[___]___[___]_[___)`-)
                          /_,~' *_\_]                 [_[(  (
                          /`. *  *\_]                 [___\ _\
                        /   `~. o \]      ;( ( ;     [_[_]`-'
                        /_ *    `~,_\    (( )( ;(;    [___]
                        /   o  *  ~'\   /\ /\ /\ /\   [_[_]
                       / *    .~~'  o\  ||_||_||_||   [___]
                      /_,.~~'`    *  _\_||_||_||_||___[_[_]_
                      /`~..  o        \:::::::::::::::::::::\
                     / *   `'~..   *   \:::::::::::::::::::::\
                    /_     o    ``~~.,,_\=========\_/========='
                    /  *      *     ..~'\         _|_ .-_--.
                   /*    o   _..~~`'*   o\           ( (_)  )
                   `-.__.~'`'   *   ___.-'            `----'
                         ":-------:"
                      hjw  \_____/
                      """


    def thebot(self, results, lastid):
        self.results = results
        self.lastid = lastid
        repliedTo = []
        for statusObj in self.results:

        ### xmas countdown added after this
            now = datetime.datetime.now()
            xmas = datetime.datetime(2014,12,25,00,00)

            take = xmas - now

            start = now
            finish = xmas
            math = finish - start
            final = ':'.join(str(math).split(':')[:2])
            first = int(math.seconds) / 60
            hour = first / 60
            extra = hour * 60
            final = first - extra
            seconds = extra * 60
            takeseconds  = math.seconds - seconds
            finalseconds = final * 60
            finalseconds = takeseconds - finalseconds
            
            left_xmas = '%r days %r hours %r minutes %r seconds till xmas' % (take.days, hour, final, finalseconds)

            print 'Posting in reply to @%s: %s' % (statusObj.user.screen_name.encode('ascii', 'replace'), statusObj.text.encode('ascii', 'replace'))
            self.api.PostUpdate('@%s %r' % (statusObj.user.screen_name, left_xmas), in_reply_to_status_id=statusObj.id)
            repliedTo.append( (statusObj.id, statusObj.user.screen_name, statusObj.text.encode('ascii', 'replace')) )
            
            print 'writing lastestfile'        
            fp = open(self.LATESTFILE, 'w')
            fp.write(str(max([x.id for x in self.results])))
            fp.close()
            
            print 'writing logfile'
            fp = open(self.LOGFILE, 'a')
            fp.write('\n'.join(['%s|%s|%s' % (x[0], x[1], x[2]) for x in repliedTo]) + '\n')
            fp.write('\n')
            fp.close()

if __name__ == '__main__':
    begin = Xmas()
    begin.xmas_ascii()
    print strftime('%H:%M:%S')
    fp = open(begin.LATESTFILE)
    lastid = fp.read().strip()
    fp.close()
    search = '#xmasbot'
    print "Searching twitter for %r" % search
    results = begin.api.GetSearch(search, since_id=lastid)
    print 'Found %s results.' % (len(results))
    begin.thebot(results, lastid)
