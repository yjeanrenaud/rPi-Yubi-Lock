#!/usr/bin/env python
# -*- coding: latin-1 -*-
# This is the main python script, which will run in an endless loop and wait for a valid yubikey to sent its otp via nfc.
# prerquisites: nfc reciever configured to work via nfcpy (kill mod nfc and pn533 for instance) on a raspberry pi with latest raspbian installed.
# hardware required: any usb nfc adapter should work. 
# standard relais module for rPi connected via gpio, thuis wiringPi is required (git.drogon.net/wiringPi) p
# CC2.0 sa-by licence. Yves Jeanrenaud. yves.jeanrenaud@gmail.com
from pprint import pprint

import nfc
import nfc.ndef
from yubico_client import Yubico
from subprocess import call

with nfc.ContactlessFrontend('usb') as clf:
        tag = clf.connect(rdwr={'on-connect': None})
#       print tag.ndef.message if tag.ndef else "Sorry, no NDEF"
        message = tag.ndef.message
#       pprint(record)
        print tag.ndef.readable
        for index, record in enumerate(message):
                rcount = " [record {0}]".format(index+1)
                try:
                        if record.type == "urn:nfc:wkt:U":
                                print("URI Record" + rcount)
                                record = nfc.ndef.UriRecord(record)
                        else:
                                print("Unknown Record Type" + rcount)
                except nfc.ndef.FormatError as e:
                         print(record.pretty(indent=2))
#        print nfc.ndef.Message(record)
#        print record
#now verify this
client = Yubico('client id', 'secret key') #get this from https://upgrade.yubico.com/getapikey/
if client.verify(record):
	call ("gpio","-g mode 23 out")
	call ("gpio","-g write 23 1")#opened relais
else print "failed to verify"
	call ("gpio","-g mode 23 out")
	call ("gpio","-g write 23 0")#closed relais