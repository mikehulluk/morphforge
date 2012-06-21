#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  - Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------------
import ConfigParser, os


class RCMgr(object):
    rcFilename = os.path.expanduser("~/.morphforgerc")
    rcConfParser = None

    @classmethod
    def has_config(cls):
        return os.path.exists(cls.rcFilename)


    @classmethod
    def get_config(cls):
        if not cls.rcConfParser:
            cls.rcConfParser = ConfigParser.SafeConfigParser()
            if not os.path.exists(cls.rcFilename):
                raise Exception("The resource file: %s does not exist!" % cls.rcFilename)
            cls.rcConfParser.read([  cls.rcFilename ])
        return cls.rcConfParser



    #Expose the same interface as the config parser does:
    @classmethod
    def has(cls, section, option):
        return cls.get_config().has_option(section, option)

    @classmethod
    def get(cls, section, option):
        return cls.get_config().get(section, option)


    #@classmethod
    #def get_int(cls, section, option):
    #    return cls.get_config().getint(section, option)

    #@classmethod
    #def get_float(cls, section, option):
    #    return cls.get_config().getfloat(section, option)


