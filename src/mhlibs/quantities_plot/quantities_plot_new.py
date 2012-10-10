#!/usr/bin/python
# -*- coding: utf-8 -*-

# ---------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  - Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------


import quantities as pq

from decimal import Decimal



def is_number_roundable_to(num, n):
    return abs(num - round(num, n)) < 0.000000001


def get_max_rounding(num):
    for i in range(0, 10):
        if is_number_roundable_to(num, i):
            return i
    assert False

def get_max_rounding_list(nums):
    for obj in nums:
        assert isinstance(obj, (int, float))
    roundings = [get_max_rounding(obj) for obj in nums]
    max_round = max(roundings)
    return max_round










class ScalarFormatterWithUnit(object):
    def __init__(self, scaling, symbol=None, ax=None, mode=None,xy=None):
        self.scaling = scaling
        self.symbol = symbol

        assert ax is not None
        self.ax = ax

        self.mode = mode
        self.xy=xy


    def __call__(self, x, pos):

        x = x * float(self.scaling)

        d = Decimal(str(x))
        num_str = "%s" % d.to_eng_string()

        if self.xy=='x':
            unit_str = "%s" % self.symbol if self.ax.units_in_ticksx and self.symbol else ""
        elif self.xy=='y':
            unit_str = "%s" % self.symbol if self.ax.units_in_ticksy and self.symbol else ""
        else:
            assert False
        return num_str + unit_str





class QuantitiesAxisNew(object):

    def getSymbolFromUnit(self, u):
        if not u:
            return " (??)"

        s = u.dimensionality.string
        if s == 'dimensionless':
            return ''
        return '%s'%s

    def xTickFormatGenerator(self, scaling, symbol, ):

        from matplotlib.ticker import FuncFormatter
        return FuncFormatter(ScalarFormatterWithUnit(scaling=scaling, symbol=symbol, ax=self, xy='x'))

    def yTickFormatGenerator(self, scaling, symbol, ):

        from matplotlib.ticker import FuncFormatter
        return FuncFormatter(ScalarFormatterWithUnit(scaling=scaling, symbol=symbol, ax=self, xy='y'))




    def __init__(self, ax, units_in_label=True, units_in_ticks=False):
        self.xyUnitBase = [None, None]
        self.xyUnitDisplay = [None, None]

        self.ax = ax
        assert self.ax


        self.safetychecking = True

        self.units_in_labelx = units_in_label
        self.units_in_labely = units_in_label
        self.units_in_ticksx = units_in_ticks
        self.units_in_ticksy = units_in_ticks

        # Store these internally, so we can
        # reapply them if units change:
        self.labelX = "<NotSet>"
        self.labelY = "<NotSet>"
        self.ax.margins(0.05,0.05)



    def _setxyUnitBase(self, unitX=None, unitY=None):
        from morphforge.stdimports import unit
        if unitX is not None:
            unitX = (unit(unitX) if isinstance(unitX, basestring) else unitX)
        if unitY is not None:
            unitY = (unit(unitY) if isinstance(unitY, basestring) else unitY)

        if unitX is not None:
            assert self.xyUnitBase[0] == None
            unitX = (unit(unitX) if isinstance(unitX, basestring) else unitX)
            self.xyUnitBase[0] = unitX.units.simplified.units
        if unitY is not None:
            assert self.xyUnitBase[1] == None
            unitY = (unit(unitY) if isinstance(unitY, basestring) else unitY)
            self.xyUnitBase[1] = unitY.units.simplified.units

    def _setxyUnitDisplay(self, unitX=None, unitY=None):
        from morphforge.stdimports import unit
        if unitX is not None:
            unitX = (unit(unitX) if isinstance(unitX, basestring) else unitX)
        if unitY is not None:
            unitY = (unit(unitY) if isinstance(unitY, basestring) else unitY)


        # Set the base units, if they are not already set:
        if unitX is not None and self.xyUnitBase[0] is None:
            self._setxyUnitBase(unitX=unitX)
        if unitY is not None and self.xyUnitBase[1] is None:
            self._setxyUnitBase(unitY=unitY)


        if unitX is not None:
            self.xyUnitDisplay[0] = unitX.units

            # Update the axis ticks:
            symbol = self.getSymbolFromUnit(self.xyUnitDisplay[0])
            scaling = (self.xyUnitBase[0]/self.xyUnitDisplay[0]).rescale(pq.dimensionless)
            xFormatterFunc = self.xTickFormatGenerator(scaling=scaling, symbol=symbol)
            self.ax.xaxis.set_major_formatter(xFormatterFunc)

        if unitY is not None:

            self.xyUnitDisplay[1] = unitY.units

            symbol = self.getSymbolFromUnit(self.xyUnitDisplay[1])
            scaling = (self.xyUnitBase[1]/self.xyUnitDisplay[1]).rescale(pq.dimensionless)
            yFormatterFunc = self.yTickFormatGenerator(scaling=scaling, symbol=symbol)
            self.ax.yaxis.set_major_formatter(yFormatterFunc)

        # Update the labels
        self._update_labels()


    def plot(self, x, y, *args, **kwargs):

        if self.xyUnitDisplay[0] is None:
            self._setxyUnitDisplay(unitX=x.units)

        if self.xyUnitDisplay[1] is None:
            self._setxyUnitDisplay(unitY=y.units)


        # Convert the incoming Data:
        x_mag = x.rescale(self.xyUnitBase[0]).magnitude
        y_mag = y.rescale(self.xyUnitBase[1]).magnitude

        # Do the plotting:
        return self.ax.plot(x_mag, y_mag, *args, **kwargs)


    # Setting limits should now be done with units:
    def set_xlim(self, *args, **kwargs):
        x0 = x1 = None
        if args is not None:
            if len(args) == 1:
                x0, x1 =args[0]
            else:
                x0, x1 = args
        else:
            x0 = kwargs.get('left', None)
            x1 = kwargs.get('right', None)

        # So we can forward arguments:
        if 'left' in kwargs:
            del kwargs['left']
        if 'left' in kwargs:
            del kwargs['left']


        #
        if x0 is not None and isinstance(x0, basestring):
            from morphforge.stdimports import unit
            x0 = unit(x0)
        if x1 is not None and isinstance(x1, basestring):
            from morphforge.stdimports import unit
            x1 = unit(x1)

        # Are the baseunits set? If not, then lets set them:
        if self.xyUnitBase[0] is None:
            self._setxyUnitDisplay(unitX=x0)


        # Set the limits
        if x0 is not None:
            self.ax.set_xlim(left = x0.rescale(self.xyUnitBase[0]).magnitude, **kwargs)
        if x1 is not None:
            self.ax.set_xlim(right =  x1.rescale(self.xyUnitBase[0]).magnitude, **kwargs)




    def set_xaxis_visible(self, visible):
        return self.ax.get_yaxis().set_visible(visible)
    def set_yaxis_visible(self, visible):
        return self.ax.get_yaxis().set_visible(visible)


    def set_xticklabel_mode(self, show_ticks=None, include_units=None, ):
        assert show_ticks in [None,True,False]
        assert include_units in [None,True,False]
        symbol = self.getSymbolFromUnit(self.xyUnitDisplay[0])
        scaling = (self.xyUnitBase[0]/self.xyUnitDisplay[0]).rescale(pq.dimensionless)

        if show_ticks is not None:
            self.units_in_ticksy = show_ticks
        if include_units is not None:
            symbol=symbol if include_units else None

        # Update the axis ticks:
        xFormatterFunc = self.xTickFormatGenerator(scaling=scaling, symbol=symbol)
        self.ax.xaxis.set_major_formatter(xFormatterFunc)


    def set_yticklabel_mode(self, show_ticks=None, include_units=None ):
        assert show_ticks in [None,True,False]
        assert include_units in [None,True,False]
        symbol = self.getSymbolFromUnit(self.xyUnitDisplay[1])
        scaling = (self.xyUnitBase[1]/self.xyUnitDisplay[1]).rescale(pq.dimensionless)

        if show_ticks is not None:
            self.units_in_ticksy = show_ticks
        if include_units is not None:
            symbol=symbol if include_units else None

        # Update the axis ticks:
        yFormatterFunc = self.yTickFormatGenerator(scaling=scaling, symbol=symbol)
        self.ax.yaxis.set_major_formatter(yFormatterFunc)













    def set_ylim(self, *args, **kwargs):
        x0 = x1 = None
        if args is not None:
            if len(args) == 1:
                x0, x1 = args[0]
            else:
                x0, x1 = args
        else:
            x0 = kwargs.get('bottom', None)
            x1 = kwargs.get('top', None)

        # So we can forward arguments:
        if 'bottom' in kwargs:
            del kwargs['bottom']
        if 'top' in kwargs:
            del kwargs['top']

        #Convert strings to units
        if x0 is not None and isinstance(x0, basestring):
            from morphforge.stdimports import unit
            x0 = unit(x0)
        if x1 is not None and isinstance(x1, basestring):
            from morphforge.stdimports import unit
            x1 = unit(x1)


        # Are the baseunits set? If not, then lets set them:
        if self.xyUnitBase[1] is None:
            self._setxyUnitDisplay(unitY=x0)

        # Set the limits
        if x0 is not None:
            self.ax.set_ylim(bottom = x0.rescale(self.xyUnitBase[1]).magnitude, **kwargs)
        if x1 is not None:
            self.ax.set_ylim(top =  x1.rescale(self.xyUnitBase[1]).magnitude, **kwargs)


    def _update_labels(self):

        # X-label
        if not self.labelX:
            self.ax.set_xlabel(self.labelX)

        elif self.units_in_labelx:
            unit_str = self.getSymbolFromUnit(self.xyUnitDisplay[0]) if self.xyUnitDisplay[0] is not None else "??"
            self.ax.set_xlabel("%s %s"%(self.labelX, (' (%s)' %unit_str if unit_str else '')))
        else:
            self.ax.set_xlabel(self.labelX)

        # Y-label
        if not self.labelY:
            self.ax.set_ylabel(self.labelY)
        elif self.units_in_labely:
            unit_str = self.getSymbolFromUnit(self.xyUnitDisplay[1]) if self.xyUnitDisplay[1] is not None else "??"
            self.ax.set_ylabel("%s %s"%(self.labelY, (' (%s)'%unit_str if unit_str else '')))
        else:
            self.ax.set_ylabel(self.labelY)

    def set_xlabel(self, xlabel):
        self.labelX = xlabel
        self._update_labels()
    def set_ylabel(self, ylabel):
        self.labelY = ylabel
        self._update_labels()

    def set_yaxis_maxnlocator(self, n):
        import matplotlib as mpl
        self.ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(n))

    def set_xaxis_maxnlocator(self, n):
        import matplotlib as mpl
        self.ax.xaxis.set_major_locator(mpl.ticker.MaxNLocator(n))

    def set_xaxis_fixedlocator(self, xticks):
        import matplotlib as mpl
        values = [float(f.rescale(self.xyUnitBase[0]).magnitude) for f in xticks]
        self.ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(values))

    def set_yaxis_fixedlocator(self, yticks):
        import matplotlib as mpl
        values = [float(f.rescale(self.xyUnitBase[1]).magnitude) for f in yticks]
        self.ax.yaxis.set_major_locator(mpl.ticker.FixedLocator(values))

    # These handle is the ticks and labels are top/bottom off the
    # graphs:
    def set_xaxis_ticks_position(self, pos):
            self.ax.xaxis.set_ticks_position(pos)
    def set_xaxis_label_position(self, pos):
            self.ax.xaxis.set_label_position(pos)

    # Spanning:
    def axvspan(self, xmin, xmax, ymin=0, ymax=1, **kwargs):
        assert self.xyUnitBase[0] is not None and self.xyUnitBase[1] is not None
        xmin_mag = xmin.rescale(self.xyUnitBase[0]).magnitude
        xmax_mag = xmax.rescale(self.xyUnitBase[0]).magnitude
        return self.ax.axvspan(xmin_mag, xmax_mag, ymin, ymax, **kwargs)

    # Spanning:
    def axvline(self, x=0, ymin=0, ymax=1, **kwargs):
        assert self.xyUnitBase[0] is not None and self.xyUnitBase[1] is not None
        x_mag = x.rescale(self.xyUnitBase[0]).magnitude
        return self.ax.axvline(x_mag, ymin, ymax, **kwargs)

    def axhline(self, y=0, xmin=0, xmax=1, **kwargs):
        assert self.xyUnitBase[0] is not None and self.xyUnitBase[1] is not None
        y_mag = y.rescale(self.xyUnitBase[1]).magnitude
        return self.ax.axhline(y_mag, xmin, xmax, **kwargs)



    def set_xunit(self, u):
        self.set_display_unit(x=u)

    def set_yunit(self, u):
        self.set_display_unit(y=u)

    def set_display_unit(self, x=None, y=None):
        self._setxyUnitDisplay(unitX=x, unitY=y)


    def __getattr__(self, name):
        protected_objects = ['xaxis', 'yaxis',
                             'transData', 'transAxes',
                             'bar', 'hist']

        # Make sure certain functions are not touched:
        if name in protected_objects and self.safetychecking:
            raise ValueError('Quantities Figure plays with "axis" to properly display values, calling functions on it directly it might have surprise consequences!')

        else:
            # Otherwise, forward it on to the original Axes object
            return getattr(self.ax, name)



    def __str__(self):
        return "<QuantitiesAxisNew: DisplayUnit:'%s' >" % (self.xyUnitDisplay)

class QuantitiesFigureNew(object):

    def __init__(self, subplot_class, *args, **kwargs):
        """Subplot_class is a class so, that we can change the subclass type that is generated. """
        import pylab
        self.fig = pylab.figure(*args, **kwargs)
        self.subplot_class = subplot_class

    def add_subplot(self, *args, **kwargs):
        subplot_ax = self.fig.add_subplot(*args, **kwargs)
        assert subplot_ax

        # Create a proxy object, that acts like an axes object, but
        # intercepts certain calls:
        return self.subplot_class(subplot_ax)

    def add_axes(self, *args, **kwargs):
        subplot_ax = self.fig.add_axes(*args, **kwargs)
        assert subplot_ax

        # Create a proxy object, that acts like an axes object, but
        # intercepts certain calls:
        return self.subplot_class(subplot_ax)
    def __getattr__(self, name):
        return getattr(self.fig, name)






