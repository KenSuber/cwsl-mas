#!/opt/cloudapps/python-vlab/ep1_2/2.7.5/bin/python
#
# #!/usr/bin/python
# doesn't work with python2.6.6; works with python2.7.5


"""

Dynamic widget to do the "data selection" step
Put the CheckBox widgets in a "scroll area" (there could be many)

Note:  there should be nothing printed to stdout when this is called in VisTrails

"""

import sys
import os
import glob
import time

from collections import OrderedDict
from PyQt4 import QtGui, QtCore
from functools import partial

dataSelectionWidth = 1200
dataSelectionHeight = 600

# Policies that use up as much space as possible:
expanding0 = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
expanding0.setVerticalStretch(0)
expanding1 = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
expanding1.setVerticalStretch(1)
expanding2 = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
expanding2.setVerticalStretch(999)
expanding3 = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
expanding3.setHorizontalStretch(1)
expanding3.setVerticalStretch(1)

# Policy that shrinks in X and Y as much as possible (?):
shrinkXY = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)

# Policy that shrinks in Y as much as possible (?):
shrinkY = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)

buttonSizeHint = QtCore.QSize(30,10)		# seems to have no effect
scrollAreaSizeHint = QtCore.QSize(50,dataSelectionHeight)		# seems to have no effect

def waitWidget(parent=None, duration=None):
    print "waitWidget:  create; duration = %s ..." % duration
    # text, ok = QtGui.QInputDialog.getText(parent, 'Input Dialog', 'Enter your name:')

    #widget = QtGui.QMessageBox(QtGui.QMessageBox.Information, "Please wait", "Please wait ...", parent=parent)
    #layout = QtGui.QVBoxLayout()
    #widget.setLayout(layout)
    #widget.show()

    layout = QtGui.QVBoxLayout()
    widget = QtGui.QMessageBox(QtGui.QMessageBox.Information, "waitWidget", "Please wait ...", parent=parent)
    layout.addWidget(widget)
    widget.show()

    print "waitWidget:  isModal = %s" % widget.isModal()
    print "waitWidget:  isVisible = %s" % widget.isVisible()
    print "waitWidget:  parent = %s" % widget.parent()
    print "waitWidget:  parentWidget = %s" % widget.parentWidget()

    if duration is not None:
        time.sleep(duration)
        widget.close()

    return widget

# Get the "choices" in the filesystem, given the specified root and branch_groups (if count_files, just count the *.nc files)
def getChoices(root, branch_groups, caller, count_files=False, verbose=False):		# branch_groups is a list of lists
    if verbose:  print 'getChoices:  root = %s, branch_groups = %s, count_files = %s' % (root, branch_groups, count_files)

    #wait = waitWidget(parent=caller)		# make a "wait" modal window appear
    #wait = waitWidget(parent=None, duration=3)		# make a "wait" modal window appear
    # caller.layout().addWidget(wait)		# caller has no layout
    #wait.show()
    #saveCursor = caller.cursor()
    #waitCursor = QtGui.QCursor()
    #waitCursor.setShape(QtCore.Qt.WaitCursor)
    #caller.setCursor(waitCursor)

    full_paths = [root]
    prefix = root
    for branch_group in branch_groups:
        if verbose:  print 'getChoices:  full_paths = %s, branch_group = %s' % (full_paths, branch_group)
        found = []				# full paths
        for branch in branch_group:
            for full_path in full_paths:
                new_path = os.path.join(full_path, branch)
                #if os.path.isdir(new_path) or os.path.islink(new_path):	# assume that a link is to a dir!
                if os.path.isdir(new_path):
                    if verbose:  print 'getChoices:  found %s in %s' % (branch, full_path)
                    found.append(new_path)
                else:
                    if verbose:  print 'getChoices:  did not find %s in %s' % (branch, full_path)
        full_paths = found
        if verbose:  print 'getChoices:  done branch_group %s; %s full_paths:' % (branch_group, len(full_paths))
        if verbose:
            for full_path in full_paths: print '\t' + full_path
    if verbose:  print 'getChoices:  done the branch_groups'

    result = set()
    for full_path in full_paths:
        if verbose:  print 'getChoices:  full_path = %s' % full_path
        if count_files:
            found = glob.glob(os.path.join(full_path, '*.nc'))		# full pathnames
            if verbose:  print 'getChoices:  found %s files:' % len(found)
            for leaf in found:
                leaf_basename = os.path.basename(leaf)
                # Add the "leaf" if not a dir (symlink OK):
                if os.path.isdir(leaf):
                    if verbose:  print "\t%s not added (a dir)" % leaf_basename
                elif os.path.islink(leaf):
                    result.add(leaf_basename)
                    if verbose:  print "\t%s added (a symlink)" % leaf_basename
                else:
                    result.add(leaf_basename)
                    if verbose:  print "\t%s added (a regular file)" % leaf_basename
        else:
            found = glob.glob(os.path.join(full_path, '*'))		# full pathnames
            if verbose:  print 'getChoices:  found %s files:' % len(found)
            for leaf in found:
                # Add the "leaf" if a dir (but not a symlink):
                leaf_basename = os.path.basename(leaf)
                if os.path.islink(leaf):
                    if verbose:  print "\t%s not added (a symlink)" % leaf_basename		# CMIP5/RCM, e.g.
                elif os.path.isdir(leaf):
                    result.add(leaf_basename)
                    if verbose:  print "\t%s added (a dir)" % leaf_basename
                else:
                    if verbose:  print "\t%s not added (not a dir)" % leaf_basename

    if count_files:
        result = len(result)
    else:
        result = list(result)
        result.sort()

    if verbose:  print 'getChoices:  result = %s' % result
    #wait.close()
    #caller.setCursor(saveCursor)
    return result

def sizing(name, obj):
    return
    if obj:
        print '(sizing) %s:  sizeHint = %s %s; sizePolicy(%s) = x: %s, %s; y: %s, %s; size = %s, %s' % (name, obj.sizeHint().width(), obj.sizeHint().height(), obj.sizePolicy().controlType(), obj.sizePolicy().horizontalPolicy(), obj.sizePolicy().horizontalStretch(), obj.sizePolicy().verticalPolicy(), obj.sizePolicy().verticalStretch(), obj.width(), obj.height())
    else:
        print '(sizing) %s:  <None>' % name

class MyPushButton(QtGui.QPushButton):
    """
    Widget for a PushButton with my defaults
    """

    def __init__(self, name, verbose=False):			# name:  str
        super(MyPushButton, self).__init__(name, sizePolicy=shrinkY, sizeHint=buttonSizeHint)

    def sizeHint(self):
        return QtCore.QSize(30, 16)		# not too wide

class ChoicesWidget(QtGui.QScrollArea):
    """
    Widget to hold the choices for a single parameter
    """

    def __init__(self, name, choices, verbose=False):			# name:  str; choices:  list of str
        super(ChoicesWidget, self).__init__(sizePolicy=expanding2)
        self.initUI(name, choices, verbose=verbose)

    def initUI(self, name, choices, verbose=False):
        self.name = name
        self.choices = choices
        self.setFrameShape(QtGui.QFrame.Panel)
        self.setLineWidth(2)

        # Put the QCheckBox buttons in a QGroupBox:
        #gb = QtGui.QGroupBox("Choices:", styleSheet="background: yellow", sizePolicy=shrinkXY)
        gb = QtGui.QGroupBox("Choices:", styleSheet="background: yellow")
        gb.setAlignment(QtCore.Qt.AlignRight)		# this seems to be ignored!
        gb.setFlat(True)		# this seems to have no effect
        gb.setToolTip("Choose at least one item for the '%s' parameter" % name)
        gbLayout = QtGui.QVBoxLayout(spacing=2)		# holds CheckBox buttons for one parameter
        gbLayout.setContentsMargins(1, 1, 1, 1)
        gb.setLayout(gbLayout)
        self.gbLayout = gbLayout
        sizing('gb', gb)

        self.choice_buttons = OrderedDict()
        for choice in choices:
            # if verbose:  print 'ChoicesWidget:  choice = %s' % choice
            button = QtGui.QCheckBox(choice, styleSheet="background: LightGreen", sizePolicy=shrinkY, sizeHint=buttonSizeHint)
            # button = QtGui.QCheckBox(choice)
            button.clicked.connect(partial(self.clicked, choice))
            gbLayout.addWidget(button, alignment=QtCore.Qt.AlignTop)
            sizing('CheckBox', button)
            self.choice_buttons[choice] = button

        self.setStyleSheet("background: Pink")
        #self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setObjectName(self.name)
        self.setWidget(gb)		# this must be called after adding the layout of gb
        scrollAreaLayout = QtGui.QVBoxLayout()
        scrollAreaLayout.setContentsMargins(1, 1, 1, 1)
        #scrollArea.show()
        sizing('scrollArea', self)

    def sizeHint(self):
        if self.widget():
            gbWidth = self.widget().width()
            gbHeight = self.widget().height()
            result = QtCore.QSize(gbWidth + 22, dataSelectionHeight)		# need an extra 22 pixels for the (possible) scrollbar
        else:
            result = QtCore.QSize(300, dataSelectionHeight)		# make height large
        return result
    """
    """

    def clicked(self, arg):
        #print '%s clicked ...' % arg
        pass

    # Get an OrderedDict of buttons, keyed by choice name
    def getButtons(self):
        return self.choice_buttons

    def clearAll(self):
        #print 'ChoicesWidget.clearAll:  %s ...' % self.name
        buttons = self.getButtons()
        for choice in buttons.keys():
            #print 'uncheck %s ...' % choice
            #buttons[choice].setCheckState(QtCore.Qt.Unchecked)
            buttons[choice].setChecked(False)

class ParameterWidget(QtGui.QFrame):
    """
    Widget to get the selection(s) for a single parameter
    """

    def __init__(self, name, choices, last=False, verbose=False):			# name:  str; choices:  list of str
        super(ParameterWidget, self).__init__(sizePolicy=expanding1)
        #super(ParameterWidget, self).__init__()
        self.initUI(name, choices, last=last, verbose=verbose)

    def initUI(self, name, choices, last=False, verbose=False):
        self.name = name
        self.choices = choices
        self.setFrameShape(QtGui.QFrame.Panel)
        self.setLineWidth(2)
        # layout = QtGui.QVBoxLayout()		# holds buttons for one parameter
        layout = QtGui.QVBoxLayout(spacing=2)		# holds buttons for one parameter
        # layout.setContentsMargins(1, 1, 1, 1)
        self.setLayout(layout)
        if verbose:  print 'ParameterWidget.initUI:  name = %s, choices = %s, layout = %s' % (name, choices, layout)

        label = QtGui.QLabel(name, pos=QtCore.QPoint(0,0), alignment=QtCore.Qt.AlignHCenter, styleSheet="background: LightBlue")
        label.setFrameShape(QtGui.QFrame.NoFrame)
        # label.setLineWidth(1)
        label.setMaximumHeight(30)
        layout.addWidget(label, alignment=QtCore.Qt.AlignTop)
        sizing('label', label)
        if verbose:  print 'initUI:  added label'

        # hline = QtGui.QLabel("", alignment=QtCore.Qt.AlignBottom, styleSheet="background: yellow")
        hline = QtGui.QLabel("", alignment=QtCore.Qt.AlignTop)
        hline.setFrameShape(QtGui.QFrame.HLine)
        layout.addWidget(hline, alignment=QtCore.Qt.AlignTop)
        sizing('hline', hline)

        # Add the choice buttons (in a QGroupBox, in a QScrollArea):
        choicesWidget = self.setChoices(choices, verbose=verbose)
        if choicesWidget:
            layout.addWidget(choicesWidget, alignment=QtCore.Qt.AlignTop)
        self.choicesWidget = choicesWidget		# may be None

        # Widget for vertical spacing; ensures hline widget is just under label widget
        # hline2 = QtGui.QLabel("", sizePolicy=expanding, alignment=QtCore.Qt.AlignTop, styleSheet="background: yellow")
        hline2 = QtGui.QLabel("", sizePolicy=expanding1, styleSheet="background: yellow")
        #hline2 = QtGui.QLabel("", styleSheet="background: yellow")
        # hline2 = QtGui.QLabel("", sizePolicy=expanding)
        # hline2.setFrameShape(QtGui.QFrame.HLine)
        hline2.setFrameShape(QtGui.QFrame.NoFrame)
        #layout.addWidget(hline2, alignment=QtCore.Qt.AlignBottom)		# so PushButtons are at the bottom
        layout.addWidget(hline2)
        sizing('hline2', hline2)

        buttonClear = MyPushButton("Clear", verbose=verbose)
        buttonClear.clicked.connect(self.clear)
        buttonClear.setToolTip("Clear all choices for this parameter")
        layout.addWidget(buttonClear, alignment=QtCore.Qt.AlignBottom)
        self.buttonClear = buttonClear
        sizing('buttonClear', buttonClear)

        buttonAll = MyPushButton("All", verbose=verbose)
        buttonAll.clicked.connect(self.all)
        buttonAll.setToolTip("Select all choices for this parameter")
        layout.addWidget(buttonAll, alignment=QtCore.Qt.AlignBottom)
        self.buttonAll = buttonAll
        sizing('buttonAll', buttonAll)

        if last:
            buttonNextLabel = "File Count ..."
            tooltip = "Show the number of files that match the constraints"
        else:
            buttonNextLabel = "Next"
            tooltip = "Display choices for the next parameter"
        buttonNext = MyPushButton(buttonNextLabel, verbose=verbose)
        buttonNext.clicked.connect(partial(self.next, last=last, verbose=verbose))
        buttonNext.setToolTip(tooltip)
        layout.addWidget(buttonNext, alignment=QtCore.Qt.AlignBottom)
        self.buttonNext = buttonNext
        sizing('buttonNext', buttonNext)

        if len(choices) == 0:
            if verbose:  print 'initUI:  hide %s push buttons' % name
            buttonClear.hide()
            buttonAll.hide()
            buttonNext.hide()

        if verbose:  print 'initUI:  done'

    """
    def sizeHint(self):
        return QtCore.QSize(230, dataSelectionHeight)		# make width narrow, height large
    """

    def setChoices(self, choices, verbose=False):
        if verbose:  print 'setChoices:  %s choices = %s' % (self.name, choices)
        if verbose:  print 'setChoices:  children = %s' % self.children()
        for child in self.children():
            if type(child) == ChoicesWidget:
                if verbose:  print 'setChoices:  close %s ChoicesWidget' % child.objectName()
                child.close()

        if len(choices) == 0:
            if verbose:  print 'setChoices:  no choices for %s; return' % self.name
            return None

        if len(choices) > 0:
            for child in self.children():
                if verbose:  print 'ParameterWidget:  child = %s %s' % (child.objectName(), child)
                if type(child) == MyPushButton:
                    if verbose:  print 'ParameterWidget:  show %s' % child
                    child.show()

        choicesWidget = ChoicesWidget(self.name, choices, verbose=verbose)
        return choicesWidget

    # Get an OrderedDict of buttons, keyed by choice name
    def getButtons(self):
        if self.choicesWidget:
            return self.choicesWidget.getButtons()
        else:
            return OrderedDict()

    def clear(self):      
        # print 'clear ...'
        buttons = self.getButtons()
        for button in buttons.values():
            button.setChecked(False)

    def all(self):      
        # print 'all ...'
        buttons = self.getButtons()
        for button in buttons.values():
            button.setChecked(True)

    def next(self, last=False, verbose=False):      
        # print '"%s" next ...' % self.name
        # Display next parameter
        parentWidget = self.parentWidget()
        # print 'next:  %s parentWidget = %s' % (self.name, parentWidget)
        if last:
            parentWidget.setNumFiles(parentWidget.countNC(verbose=verbose))		# number of NC files
        else:
            parentWidget.displayNext(self.name, verbose=verbose)		# calling a function in the parent; not ideal?
            parentWidget.setNumFiles(-1)

    def clearAll(self):
        #print 'ParameterWidget.clearAll:  %s ...' % self.name
        if self.choicesWidget:
            self.choicesWidget.clearAll()

class DataSelection(QtGui.QWidget):

    def __init__(self, drstree_base, parameterNames, verbose=False):			# parameterNames:  list of names
        super(DataSelection, self).__init__(minimumWidth=dataSelectionWidth, minimumHeight=dataSelectionHeight)
        if verbose:  print 'DataSelection.__init__:  verbose = %s' % verbose
        self.initUI(drstree_base, parameterNames, verbose=verbose)

    def initUI(self, drstree_base, parameterNames, verbose=False):
        if verbose:  print 'DataSelection.initUI:  verbose = %s' % verbose
        if verbose:  print 'drstree_base = %s' % drstree_base
        if verbose:  print 'parameterNames = %s' % parameterNames
        self.drstree_base = drstree_base
        self.parameterNames = parameterNames
        self.currentParameterIndex = 0
        self.result = "Not defined"
        # Create widgets and layouts; add widgets to layouts; add child layouts to parent layouts; set layout of parent widget; show
        if verbose:  print 'self.layout = %s' % self.layout()
        mainLayout = QtGui.QVBoxLayout()
        if verbose:  print 'mainLayout = %s' % mainLayout
        headerLayout = QtGui.QHBoxLayout()		# for title, etc.
        midLayout = QtGui.QHBoxLayout()			# for the parameters
        footerLayout = QtGui.QHBoxLayout()		# for DONE button, etc.

        # Create the GUI heirarchy:

        self.parameterWidgets = OrderedDict()
        for name in parameterNames[0:1]:		# first parameter
            #choices = ['choice1', 'choice2']
            choices = getChoices(self.drstree_base, [], self, verbose=verbose)
            parameterWidget = self.addParameter(midLayout, name, choices, verbose=verbose)
            self.parameterWidgets[name] = parameterWidget
        for name in parameterNames[1:-1]:		# all but first and last parameter
            parameterWidget = self.addParameter(midLayout, name, [], verbose=verbose)
            self.parameterWidgets[name] = parameterWidget
        for name in parameterNames[-1:]:		# last parameter
            parameterWidget = self.addParameter(midLayout, name, [], last=True, verbose=verbose)
            self.parameterWidgets[name] = parameterWidget

        #mainButtonSizePolicy = QtGui.QSizePolicy()
        #mainButtonSizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)		# wide
        #mainButtonSizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)		# small
        mainButtonSizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)		# smallish

        resetButton = QtGui.QPushButton("Reset", sizePolicy=mainButtonSizePolicy)
        resetButton.clicked.connect(partial(self.reset, verbose=verbose))
        resetButton.setToolTip("Clear all the selections")

        cancelButton = QtGui.QPushButton("Cancel", sizePolicy=mainButtonSizePolicy)
        cancelButton.clicked.connect(partial(self.cancel, verbose=verbose))
        cancelButton.setToolTip("Cancel the widget")

        doneButton = QtGui.QPushButton("Done", sizePolicy=mainButtonSizePolicy)
        doneButton.clicked.connect(partial(self.done, verbose=verbose))
        doneButton.setToolTip("Exit the widget")

        self.setWindowTitle('Title:  Data Selection Widget')

        self.setWindowModality(QtCore.Qt.WindowModal)

        title1 = "The Data Selection Widget:  make selections for each parameter from left to right, clicking 'Next' to move to the next parameter."
	title2 = "After making the selection for the last parameter, you may click 'File Count ...' to show how many files would match the constraints."
	title3 = "Click 'Reset' to start over; click 'Done' to exit the widget."
        title = QtGui.QLabel("%s\n%s\n%s" % (title1, title2, title3), alignment=QtCore.Qt.AlignHCenter)
        headerLayout.addWidget(title)
        sizing('title', title)

        hiddenLabel = QtGui.QLabel("", sizePolicy=expanding3, styleSheet="background: yellow")
        #hiddenLabel.setFrameShape(QtGui.QFrame.NoFrame)
        self.num_files_widget = QtGui.QLabel("initial")
        self.setNumFiles(-1)
        footerLayout.addWidget(hiddenLabel)		# wide
        footerLayout.addWidget(self.num_files_widget)
        footerLayout.addWidget(resetButton)		# small, to right
        footerLayout.addWidget(cancelButton)		# small, to right
        footerLayout.addWidget(doneButton)		# small, to right
        sizing('doneButton', doneButton)

        mainLayout.addLayout(headerLayout)
        mainLayout.addLayout(midLayout)
        mainLayout.addLayout(footerLayout)
        self.setLayout(mainLayout)
        if verbose:  print '%s widget parentWidget = %s' % ("mip", self.parameterWidgets["mip"].parentWidget())
        self.show()

        if verbose:  print 'DataSelection.initUI done'
        
    # Add a parameter selection widget to the GUI (adds the widget to parentLayout)
    def addParameter(self, parentLayout, name, choices, last=False, verbose=False):      
        if verbose:  print 'addParameter:  name = %s, choices = %s, parentLayout = %s' % (name, choices, parentLayout)
        widget = ParameterWidget(name, choices, last=last, verbose=verbose)
        parentLayout.addWidget(widget)		# all parameter widgets are the same height
        sizing(name + ' Parameter', widget)
        if verbose:  print 'addParameter:  done'
        return widget

    def displayNext(self, name, verbose=False):
        if verbose:  print 'displayNext:  name = %s' % name
        nextIndex = self.parameterNames.index(name) + 1
        if verbose:  print 'displayNext:  nextIndex = %s' % nextIndex
        if nextIndex < len(self.parameterNames):
            nextParameterName = self.parameterNames[nextIndex]
            if verbose:  print 'displayNext:  nextParameterName = %s' % nextParameterName
            nextParameterWidget = self.parameterWidgets[nextParameterName]
            # Add the choice buttons:
            # choices = getChoices(self.drstree_base, [self.getParameterSelected(name)], verbose=verbose)
            # Add results from the first ParameterWidget up thru <name>:
            branch_groups = []
            for jj in range(nextIndex):
                choices_ = self.getParameterSelected(self.parameterNames[jj])
                if verbose:  print 'displayNext:  %s choices = %s' % (self.parameterNames[jj], choices_)
                branch_groups.append(choices_)
            choices = getChoices(self.drstree_base, branch_groups, self, verbose=verbose)
            #self.setNumFiles(len(choices))		# number of leaves (of last branch)
            choicesWidget = nextParameterWidget.setChoices(choices, verbose=verbose)
            nextParameterWidget.choicesWidget = choicesWidget
            if choicesWidget:
                nextParameterWidget.layout().insertWidget(2, choicesWidget, alignment=QtCore.Qt.AlignTop)
                if verbose:  print 'choicesWidget.width() = %s, choicesWidget.height() = %s' % (choicesWidget.width(), choicesWidget.height())
        else:
            if verbose:  print 'displayNext:  no parameter after %s' % name
        #if verbose:  print 'self.width() = %s, self.height() = %s' % (self.width(), self.height())
        if verbose:		# print width of each parameter widget
            for parameterName in self.parameterNames:
                parameterWidget = self.parameterWidgets[parameterName]
                sizing('displayNext:  %s parameter widget' % parameterName, parameterWidget)
                sizing('displayNext:  %s choicesWidget' % parameterName, parameterWidget.choicesWidget)
                if parameterWidget.choicesWidget:
                    sizing('displayNext:  %s gb' % parameterName, parameterWidget.choicesWidget.widget())

    def count(self, verbose=False):
        self.setNumFiles(self.countNC(verbose=verbose))		# number of NC files

    # Reset the widget:  all choices disappear except the first
    def reset(self, verbose=False):
        name0 = self.parameterWidgets.keys()[0]
        parameterWidget = self.parameterWidgets[name0]
        choices = getChoices(self.drstree_base, [], self, verbose=verbose)
        if verbose:  print 'reset:  (%s) choices = %s' % (name0, choices)
        parameterWidget.clearAll()
        for parameterName in self.parameterWidgets.keys()[1:]:
            parameterWidget = self.parameterWidgets[parameterName]
            parameterWidget.clearAll()
            parameterWidget.setChoices([], verbose=verbose)
            parameterWidget.buttonClear.hide()
            parameterWidget.buttonAll.hide()
            parameterWidget.buttonNext.hide()

        if verbose:  print 'reset:  ConstraintString = "%s"' % self.getConstraintString()

    def cancel(self, verbose=False):
        # print 'cancel ...'
        self.reset(verbose=verbose)
        self.result = OrderedDict()
        self.setNumFiles(0)		# number of NC files
        self.close()

    def done(self, verbose=False):
        # print 'done ...'
        self.result = self.getResult()		# OrderedDict of choices
        self.setNumFiles(self.countNC(verbose=verbose))		# number of NC files
        self.close()

    def countNC(self, verbose=False):
        lastParameterName = self.parameterNames[-1]
        if verbose:  print 'countNC:  lastParameterName = %s' % lastParameterName

        # Check results from the first ParameterWidget up thru the last:
        branch_groups = []
        for jj in range(len(self.parameterNames)):
            choices_ = self.getParameterSelected(self.parameterNames[jj])
            if verbose:  print 'countNC:  %s choices = %s' % (self.parameterNames[jj], choices_)
            branch_groups.append(choices_)
        num_choices = getChoices(self.drstree_base, branch_groups, self, count_files=True, verbose=verbose)
        return num_choices		# number of *.nc files (at last "branches")

    # Get the result (i.e., a dict of all buttons) for one parameter
    def getParameterResult(self, parameterName, verbose=False):
        if verbose:  print 'getParameterResult:  parameterName = %s' % parameterName
        buttons = self.parameterWidgets[parameterName].getButtons()
        if verbose:  print 'getParameterResult:  buttons = %s' % buttons.keys()
        result = OrderedDict()
        for choice in buttons.keys():
            if verbose:  print 'getParameterResult:  choice = %s' % choice
            if verbose:  print 'getParameterResult:  button = %s' % buttons[choice]
            result[choice] = buttons[choice].isChecked()
        # if verbose:  print 'getParameterResult:  result = %s' % result
        return result

    # Get the result (i.e., the list of selected buttons) for one parameter
    def getParameterSelected(self, parameterName, verbose=False):
        result = []
        buttons = self.parameterWidgets[parameterName].getButtons()
        for choice in buttons.keys():
            if buttons[choice].isChecked():  result.append(choice)
        if verbose:  print 'getParameterSelected:  result = %s' % result
        return result

    # Get the result (i.e., the list of selected buttons) for all parameters
    def getResult(self, verbose=False):
        result = OrderedDict()
        for parameterName in self.parameterWidgets.keys():
            result[parameterName] = self.getParameterResult(parameterName)
        return result

    def getConstraintString(self):
        dictResult = self.getResult()
        result = ''
        for parameterName in dictResult.keys():
            parameterResult = dictResult[parameterName]
            # If any choices are true, add to the result:
            # numSelected = 
            # if numSelected > 0:
            if any(parameterResult.values()):
                result += parameterName + ' = '
                for choice in parameterResult.keys():
                    if parameterResult[choice]:
                        result += choice + ', '
                result = result[0:-2]			# discard last 2 chars:  ', '
                result += '; '
        if len(result) > 0:  result = result[0:-2]		# discard last 2 chars:  '; '
        return result

    def setNumFiles(self, num_files):
        self.num_files = num_files
        if num_files >= 0:
            self.num_files_widget.setText("Number of files = %s" % num_files)
        else:
            self.num_files_widget.setText("Number of files is unknown")

    def getNumFiles(self):
        return self.num_files

def main():
    # The parameters for the GUI:
    drstree_base = '/g/data/ua6/drstree'
    subdirs = ['mip', 'product', 'institute', 'model', 'experiment', 'frequency', 'realm', 'variable', 'ensemble']

    # Can start at a specific branch:
    # drstree_base = '/g/data/ua6/drstree/CMIP5/GCM'
    # subdirs = ['institute', 'model', 'experiment', 'frequency', 'realm', 'variable', 'ensemble']

    # The CMIP5/RCM sub-tree has a different structure:
    # drstree_base = '/g/data/ua6/drstree/CMIP5/RCM'
    # subdirs = ['region', 'institute', 'model', 'experiment', 'ensemble', 'model2?', 'version', 'frequency', 'variable']

    app = QtGui.QApplication(["Data Selection App"])
    font = QtGui.QFont()
    font.setPointSize(8)		# don't go less than 8
    app.setFont(font)
    #print 'DataSelectionN.py:  sys.argv = %s' % sys.argv
    if len(sys.argv) > 1:  verbose = True
    else:  verbose = False
    ds = DataSelection(drstree_base, subdirs, verbose=verbose)		# create the widget
    #wait = waitWidget(parent=None, duration=7)		# make a "wait" modal window appear
    returnCode = app.exec_()		# make the widget(s) appear, and get user input until "Done" button is pressed
    result = ds.getConstraintString()
    if verbose:  print 'ds.width() = %s, ds.height() = %s' % (ds.width(), ds.height())
    # print 'ds.getResult() = %s' % ds.getResult()
    # print 'result = "%s"' % result
    num_files = ds.getNumFiles()
    return (result, num_files)

    """

    How do we get the widget result (i.e., the ConstraintString) to a VisTrails output port, 
    so it can then be used by the next module in the pipeline?

    Use the CLTools Wizard to create a wrapper to this script; create an output port from stdout, with type = string
    """

if __name__ == '__main__':
    (constraintString, num_files) = main()

    #print constraintString		# the (only) widget result (unless 'verbose' was specified)
    print 'constraintString = "%s"' % constraintString
    print 'num_files = %s' % num_files
    #sys.exit(returnCode)		# always 0, unless the widget aborted
