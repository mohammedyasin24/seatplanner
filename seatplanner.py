#This program will help you to plan seats for an examination
#This code is released under GPL v3.So feel free to modify and distribute.
#Author:Mahesh C
#Release date:4-April-2010





__author__="mahesh"
__date__ ="$6 Apr, 2010 9:38:14 AM$"







import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from random import *





columnMax=16
yseekMax=500
debug=0
rev_stud_list=1

#Main Gui class

class Gui(QWidget):
    def __init__(self, parent=None):

        #Final result are located in this lists
        self.roomAllocation=[]
        self.rSummary=[]
        self.shuffle=1
        self.rTitle="ABCDEFGHIJKLMNOPQ"
        #Setup the gui
        QWidget.__init__(self, parent)
        self.setFixedSize(850,650)
        self.setWindowTitle('Arrange Seats')


        seLabel=QLabel(self)
        seLabel.setGeometry(10,5,100,20)
        seLabel.setText("Room Details:")
        self.seatTable=QTableWidget(self)
        self.seatTable.setRowCount(1)
        self.seatTable.setColumnCount(columnMax)
        self.seatTable.setGeometry(10,30,725,300)
        cHeaders=[QTableWidgetItem()]
        self.seatTable.setHorizontalHeaderItem(0,cHeaders[0])
        cHeaders[0].setText("Room Name")
        for i in range(1,columnMax):
            cHeaders.append(QTableWidgetItem())
            self.seatTable.setHorizontalHeaderItem(i,cHeaders[i])
            cHeaders[i].setText("Column-"+self.rTitle[i-1])

        self.addSeRowButton = QPushButton(self)
        self.addSeRowButton.setText("Add Row")
        self.addSeRowButton.setGeometry(745,30, 94, 27)
        self.delSeRowButton =  QPushButton(self)
        self.delSeRowButton.setText("Delete Row")
        self.delSeRowButton.setGeometry(745,80, 94, 27)

        stLabel=QLabel(self)
        stLabel.setGeometry(10,350,100,20)
        stLabel.setText("Students Details:")
        self.studTable=QTableWidget(self)
        self.studTable.setRowCount(1)
        self.studTable.setColumnCount(3)
        self.studTable.setGeometry(10,370,350,250)
        cHeader0=QTableWidgetItem()
        cHeader1=QTableWidgetItem()
        cHeader2=QTableWidgetItem()
        self.studTable.setHorizontalHeaderItem(0,cHeader0)
        cHeader0.setText("Batch")
        self.studTable.setHorizontalHeaderItem(1,cHeader1)
        cHeader1.setText("From")
        self.studTable.setHorizontalHeaderItem(2,cHeader2)
        cHeader2.setText("To")

        self.addStRowButton=QPushButton(self)
        self.addStRowButton.setText("Add Row")
        self.addStRowButton.setGeometry(370,370, 94, 27)
        self.delStRowButton=QPushButton(self)
        self.delStRowButton.setText("Delete Row")
        self.delStRowButton.setGeometry(370,420, 94, 27)

        sFrame=QFrame(self)
        sFrame.setGeometry(480,370,160,250)
        sFrame.setFrameShape(QFrame.StyledPanel);
        sFrame.setFrameShadow(QFrame.Raised);

        seLabel=QLabel(self)
        seLabel.setGeometry(490,380,150,20)
        seLabel.setText("No of seats")
        self.nseLabel=QLabel(self)
        self.nseLabel.setGeometry(530,400,150,20)
        self.nseLabel.setText("0")

        stLabel=QLabel(self)
        stLabel.setGeometry(490,430,150,20)
        stLabel.setText("No of students")
        self.nstLabel=QLabel(self)
        self.nstLabel.setGeometry(530,450,150,20)
        self.nstLabel.setText("0")

        self.rfrshButton =  QPushButton(self)
        self.rfrshButton.setText("Refresh")
        self.rfrshButton.setGeometry(490,470, 94, 27)

        dLabel=QLabel(self)
        dLabel.setGeometry(490,510,150,20)
        dLabel.setText("Import/Export table data")


        self.saveButton =  QPushButton(self)
        self.saveButton.setText("Export")
        self.saveButton.setGeometry(490, 540, 94, 27)
        self.loadButton =  QPushButton(self)
        self.loadButton.setText("Import")
        self.loadButton.setGeometry(490,580, 94, 27)

        rFrame=QFrame(self)
        rFrame.setGeometry(650,370,190,250)
        rFrame.setFrameShape(QFrame.StyledPanel);
        rFrame.setFrameShadow(QFrame.Raised);

        self.sCheckBox=QCheckBox(self)
        self.sCheckBox.setGeometry(670,390,150,22)
        self.sCheckBox.setText("Do not shuffle")

        self.printButton =  QPushButton(self)
        self.printButton.setText("Print Reports")
        self.printButton.setGeometry(670, 450, 94, 27)

        self.expButton =  QPushButton(self)
        self.expButton.setText("CSV Reports")
        self.expButton.setGeometry(670, 490, 94, 27)

        self.exitButton =  QPushButton(self)
        self.exitButton.setText("Exit")
        self.exitButton.setGeometry(700,600, 94, 27)
    #Define all connections
        self.connect(self.addStRowButton,SIGNAL("clicked()"),self.addStRow);
        self.connect(self.addSeRowButton,SIGNAL("clicked()"),self.addSeRow);
        self.connect(self.delSeRowButton,SIGNAL("clicked()"),self.delSeRow);
        self.connect(self.delStRowButton,SIGNAL("clicked()"),self.delStRow);
        self.connect(self.rfrshButton,SIGNAL("clicked()"),self.refreshLabels);
        self.connect(self.printButton,SIGNAL("clicked()"), self.printReports);
        self.connect(self.saveButton,SIGNAL("clicked()"),self.saveToFile);
        self.connect(self.loadButton,SIGNAL("clicked()"),self.loadFromFile);
        self.connect(self.expButton,SIGNAL("clicked()"),self.exportAsCsv);
        self.connect(self.exitButton,SIGNAL("clicked()"),self.close);
    def refreshLabels(self):
        seats=self.findTotalSeats()
        students=self.findTotalStudents()
        self.nseLabel.setText(str(seats))
        self.nstLabel.setText(str(students))

    def findTotalSeats(self):
        msgBox=QMessageBox()
        seats=0
        for i in range(0,self.seatTable.rowCount()):
            for j in range(1,columnMax):
                data=self.getTableData(self.seatTable,i,j)
                if data=="EMPTY":
                    continue
                else:
                    seats=seats+int(data)
        return seats

    def findTotalStudents(self):
        students=0
        sfrom=0
        sto=0;
        msgBox=QMessageBox()
        for i in range(0,self.studTable.rowCount()):
            if self.getTableData(self.studTable,i,0)=='EMPTY':
                msgBox.setIcon(QMessageBox.Critical)
                msgBox.setText("Batch name is mandatory")
                msgBox.exec_()
                return 0
            data=self.getTableData(self.studTable,i,1)
            if data=="EMPTY":
                msgBox.setIcon(QMessageBox.Critical)
                msgBox.setText("'From' field is empty in students details")
                msgBox.exec_()
                return 0
            else:
                sfrom=int(data)
            data=self.getTableData(self.studTable,i,2)
            if data=='EMPTY' or int(data)==sfrom:
                sto=0
                students=students+1
                continue
            elif int(data)<sfrom:
                msgBox.setIcon(QMessageBox.Critical)
                msgBox.setText("'From' field must be less than 'to' field in students details")
                msgBox.exec_()
                return 0
            else:
                sto=int(data)
                students=students+(sto-sfrom)+1
        return students




    def loadFromFile(self):
        fileName = QFileDialog.getOpenFileName(self, "Load File","","*")
        if fileName=='':
            return
        #Empty tables
        for i in range(0,self.seatTable.rowCount()):
            self.delSeRow()
        for i in range(0,self.studTable.rowCount()):
            self.delStRow()

        fp=open(fileName,'r')
        data=fp.readlines()
        list=[]
        flag=''
        if debug==1:
            print data
        tIndex=0
        for  line in data:

            temp=line.replace("\n","")
            if temp=="%studTable":
                flag='stud'
                continue
            if temp=="%seatTable":
                flag='seat'
                tIndex=0
                continue
            if flag=="stud":
                row=temp.split('#')
                self.studTable.insertRow(self.studTable.rowCount())
                self.setTableData(self.studTable,tIndex,0,row[0])
                self.setTableData(self.studTable,tIndex,1,row[1])
                self.setTableData(self.studTable,tIndex,2,row[2])
                tIndex=tIndex+1
            if flag=="seat":
                row=temp.split('#')
                if debug==1:
                    print row
                self.seatTable.insertRow(self.seatTable.rowCount())
                for i in range(0,columnMax):
                    self.setTableData(self.seatTable,tIndex,i,row[i])
                tIndex=tIndex+1




    def saveToFile(self):
        fileName = QFileDialog.getSaveFileName(self, "Save File","untitled.txt","*")
        fp=open(fileName,'w')
        fp.writelines("%studTable\n")
        for i in range(0,self.studTable.rowCount()):
            batch=self.getTableData(self.studTable,i,0)
            sfrom=self.getTableData(self.studTable,i,1)
            sto=self.getTableData(self.studTable,i,2)
            fp.writelines(batch+"#"+sfrom+"#"+sto+"\n")
        fp.writelines("%seatTable\n")
        for i in range(0,self.seatTable.rowCount()):
            for j in range(0,columnMax):
                row=self.getTableData(self.seatTable,i,j)
                if(j==columnMax-1):
                    fp.writelines(row)
                else:
                    fp.writelines(row+"#")
            fp.writelines("\n")
        fp.close()

    #functions for add and delete table rows
    def addStRow(self):
        self.studTable.insertRow(self.studTable.rowCount())
    def addSeRow(self):
        self.seatTable.insertRow(self.seatTable.rowCount())
    def delStRow(self):
        self.studTable.removeRow(self.studTable.rowCount()-1)
    def delSeRow(self):
        self.seatTable.removeRow(self.seatTable.rowCount()-1)

    def getTableData(self,table,row,col):
        temp=QTableWidgetItem()
        temp=table.item(row,col);
        if temp==None:
            return "EMPTY"
        data=temp.text().trimmed()
        if data=="":
            return "EMPTY"
        return data

    def setTableData(self,table,row,col,data):
        temp=QTableWidgetItem()
        table.setItem(row,col,temp)
        if data=="EMPTY":
            temp.setText("")
        else:
            temp.setText(data);



    def doArrangment(self):

        #Check mandatory conditions before proceed"
        msgBox=QMessageBox()
        if self.findTotalSeats()<self.findTotalStudents() or self.findTotalSeats()==0:
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText("Less seats !!")
            msgBox.exec_()
            return 0
        if self.findTotalStudents()==0:
            return 0
        self.roomAllocation=[]
        self.rSummary=[]

        #Empty all
        slist=self.createStudList()
        sallocList=[]
        sindex=0
        self.shuffle=1
        #check for shuffle
        if self.sCheckBox.checkState ()==Qt.Checked:
            self.shuffle=0
        #traverse thrgh the students list and allocate each rooms
        if self.shuffle==0:
            for i in range(0,self.seatTable.rowCount()):
                room=self.createRoom(i)
                roomName=self.getTableData(self.seatTable,i,0)
                if roomName=='EMPTY':
                    msgBox.setIcon(QMessageBox.Critical)
                    msgBox.setText("Room name is mandatory")
                    msgBox.exec_();
                    return 0
                for j in range(0,len(room[1])):
                    for k in range(0,len(room[1][j])):
                        if sindex==len(slist):
                            room[1][j][k]="EM"
                        else:
                            room[1][j][k]=[slist[sindex][0],slist[sindex][1],slist[sindex][2]]
                            sallocList.append([slist[sindex][0],slist[sindex][1],slist[sindex][2],str(roomName)])
                            sindex=sindex+1
                if debug==1:
                    print str(roomName)
                    print "allocation is"
                    print room[1]
                self.roomAllocation.append([roomName,room[1]])
        else:
            if len(slist)%2==0:
                fw_max=len(slist)/2
                bwd_max=len(slist)/2
            else:
                fw_max=len(slist)/2+1
                bwd_max=len(slist)/2
            fwi=0
            bwi=len(slist)-1
            f_finished=0
            b_finished=0
            if debug==1:
                print "Slist to allocate is ",slist
            for i in range(0,self.seatTable.rowCount()):
                room=self.createRoom(i)
                if debug==1:
                    print "Created room is",room
                roomName=self.getTableData(self.seatTable,i,0)
                if roomName=='EMPTY':
                    msgBox.setIcon(QMessageBox.Critical)
                    msgBox.setText("Room name is mandatory")
                    msgBox.exec_();
                    return 0
                for j in range(0,len(room[1])):
                    for k in range(0,len(room[1][j])):
                        if debug==1:
                            print "room index j",k
                        if bwi<=len(slist)-1-bwd_max:
                            if debug==1:
                                print "end of bwd",i,j
                            b_finished=1
                        else:
                            if j%2!=0 and f_finished==0:
                                if debug==1:
                                    print "bwd in odd",j,bwi,"appending data",[slist[bwi][0],slist[bwi][1],slist[bwi][2]]
                                room[1][j][k]=[slist[bwi][0],slist[bwi][1],slist[bwi][2]]
                                sallocList.append([slist[bwi][0],slist[bwi][1],slist[bwi][2],str(roomName)])
                                bwi=bwi-1
                                continue
                        if fwi>fw_max-1:
                            if debug==1:
                                print "end of fwd",i,j
                            f_finished=1
                        else:
                            if j%2==0 and b_finished==0:
                                if debug==1:
                                    print "fwd in even",j,fwi,"appending data",[slist[fwi][0],slist[fwi][1],slist[fwi][2]]
                                room[1][j][k]=[slist[fwi][0],slist[fwi][1],slist[fwi][2]]
                                sallocList.append([slist[fwi][0],slist[fwi][1],slist[fwi][2],str(roomName)])
                                fwi=fwi+1
                                continue
                        if f_finished==1 and  b_finished==0:
                                if debug==1:
                                    print "bwd in fwd_finished",j,bwi,"appending data",[slist[bwi][0],slist[bwi][1],slist[bwi][2]]
                                room[1][j][k]=[slist[bwi][0],slist[bwi][1],slist[bwi][2]]
                                sallocList.append([slist[bwi][0],slist[bwi][1],slist[bwi][2],str(roomName)])
                                bwi=bwi-1
                                continue
                                
                        if b_finished==1 and f_finished==0:
                                if debug==1:
                                    print "fwd in bwd_finished",j,fwi,"appending data",[slist[fwi][0],slist[fwi][1],slist[fwi][2]]
                                room[1][j][k]=[slist[fwi][0],slist[fwi][1],slist[fwi][2]]
                                sallocList.append([slist[fwi][0],slist[fwi][1],slist[fwi][2],str(roomName)])
                                fwi=fwi+1
                                continue
                        
                        if f_finished==1 and b_finished==1:
                            room[1][j][k]="EM"
                        

                if debug==1:
                    print "allocation is"
                    print "room:",roomName,"Data",room[1]
                self.roomAllocation.append([roomName,room[1]])




        #traverse thrgh the students allocated list and find a consolidated report
        clsalloc=[]
        bList=[]

        for i in range(0,self.studTable.rowCount()):
            clsalloc=[]
            min=0
            max=0
            branch=str(self.getTableData(self.studTable,i,0))
            #check the branch have duplicate
            found=0
            for s in bList:
                if s==branch:
                    found=1
            if found==1:
                continue
            bList.append(branch)
            for j in range(0,len(sallocList)):
                if sallocList[j][0]==branch:
                    clsalloc.append(sallocList[j])
            if debug==1:
                print "clsalloc is",clsalloc
            for j in range(0,self.seatTable.rowCount()):
                roomName=str(self.getTableData(self.seatTable,j,0))
                temp=[]
                for k in range(0,len(clsalloc)):
                    if clsalloc[k][3]==roomName:
                        temp.append(clsalloc[k][1])

                if(len(temp)>0):
                    temp.sort()
                    small=temp[0]
                    if debug==1:
                        print "temp after sort is",temp
                    for s in range(1,len(temp)):
                        if temp[s]-temp[s-1]==1:
                            if debug==1:
                                print "eq",s,temp[s-1],temp[s]
                            continue
                        else:
                            if debug==1:
                                print "strip",s,temp[s-1],temp[s]
                            self.rSummary.append([branch,small,temp[s-1],roomName])
                            small=temp[s]
                    #if the last element alone will make problem without shuffle
                    if len(temp)==1:
                        self.rSummary.append([branch,small,small,roomName])
                    else:
                        self.rSummary.append([branch,small,temp[s],roomName])


            if debug==1:
                print "summary report is"
                print  self.rSummary
        return 1



    def printReports(self):

        if self.doArrangment()==0:
            return 0
        xseek=10
        yseek=10
        res=1024
        rowWidth=35
        colWidth=35
        ixseek=xseek
        iyseek=yseek
        oxseek=xseek
        oyseek=yseek
        printer=QPrinter()
        painter=QPainter()
        rect=QRect()

        pdialog=QPrintDialog(printer)
        if pdialog.exec_()==QDialog.Accepted:
            printer.setOrientation(QPrinter.Landscape)
            painter.begin(printer)
            for room in  self.roomAllocation:
                painter.setFont(QFont("Arial",20));
                #Row titles
                rTitle=self.rTitle
                tIndex=0
                #Draw the Top header - room name
                roomName=room[0]
                rect.setRect(xseek,yseek,res,rowWidth)
                painter.drawRect(rect)
                painter.drawText(rect, Qt.AlignCenter,roomName)
                yseek=yseek+rowWidth
                ixseek=xseek
                iyseek=yseek
                colWidth=res/(len(room[1])+1)
                #find the largest column and draw serial numbers
                largest=0
                for row in room[1]:
                    if len(row)>largest:
                        largest=len(row)

                #One empty cell
                yseek=yseek+rowWidth

                for i in range(1,largest+1):
                    rect.setRect(xseek,yseek,colWidth,rowWidth)
                    painter.drawRect(rect)
                    painter.drawText(rect, Qt.AlignCenter,str(i))
                    yseek=yseek+rowWidth

                yseek=iyseek
                xseek=xseek+colWidth

                #Draw a all rows
                painter.setFont(QFont("Arial",15));
                for row in room[1]:

                    #Draw the row title
                    rect.setRect(xseek,yseek,colWidth,rowWidth)
                    painter.drawRect(rect)
                    painter.drawText(rect, Qt.AlignCenter,rTitle[tIndex])
                    yseek=yseek+rowWidth
                    tIndex=tIndex+1
                    #Draw cells
                    for cell in row:
                        if debug==1:
                            print "cell is",cell
                        rect.setRect(xseek,yseek,colWidth,rowWidth)
                        painter.drawRect(rect)
                        if cell=="EM":
                            painter.drawText(rect, Qt.AlignCenter,'-')
                        else:
                           painter.drawText(rect, Qt.AlignCenter,cell[0]+"-"+str(cell[1]))
                        yseek=yseek+rowWidth
                    yseek=iyseek
                    xseek=xseek+colWidth
                printer.newPage()
                xseek=oxseek
                yseek=oyseek

            #print summary reports
            pen=QPen(Qt.black, 2)
            painter.setPen(pen)
            xseek=oxseek
            yseek=oyseek
            colWidth=res/3
            rect.setRect(xseek,yseek,res,rowWidth)
            painter.drawRect(rect)
            painter.drawText(rect, Qt.AlignCenter,"Summary of room allocation")
            yseek=yseek+rowWidth
            #xseek=ixseek
            rect.setRect(xseek,yseek,colWidth,rowWidth)
            painter.drawRect(rect)
            painter.drawText(rect, Qt.AlignCenter,"Branch")
            xseek=xseek+colWidth
            rect.setRect(xseek,yseek,colWidth,rowWidth)
            painter.drawRect(rect)
            painter.drawText(rect, Qt.AlignCenter,"From-To")
            xseek=xseek+colWidth
            rect.setRect(xseek,yseek,colWidth,rowWidth)
            painter.drawRect(rect)
            painter.drawText(rect, Qt.AlignCenter,"Room")
            yseek=yseek+rowWidth
            xseek=ixseek
            for row in self.rSummary:
                if debug==1:
                    print "for a row"
                    print row[0]
                    print xseek
                    print yseek
                if yseek>=yseekMax:
                    printer.newPage()
                    xseek=oxseek
                    yseek=oyseek
                    colWidth=res/3
                    rect.setRect(xseek,yseek,res,rowWidth)
                    painter.drawRect(rect)
                    painter.drawText(rect, Qt.AlignCenter,"Summary of room allocation")
                    yseek=yseek+rowWidth
                    rect.setRect(xseek,yseek,colWidth,rowWidth)
                    painter.drawRect(rect)
                    painter.drawText(rect, Qt.AlignCenter,"Branch")
                    xseek=xseek+colWidth
                    rect.setRect(xseek,yseek,colWidth,rowWidth)
                    painter.drawRect(rect)
                    painter.drawText(rect, Qt.AlignCenter,"From-To")
                    xseek=xseek+colWidth
                    rect.setRect(xseek,yseek,colWidth,rowWidth)
                    painter.drawRect(rect)
                    painter.drawText(rect, Qt.AlignCenter,"Room")
                    yseek=yseek+rowWidth
                    xseek=ixseek
                rect.setRect(xseek,yseek,colWidth,rowWidth)
                painter.drawRect(rect)
                painter.drawText(rect, Qt.AlignCenter,row[0])
                xseek=xseek+colWidth
                rect.setRect(xseek,yseek,colWidth,rowWidth)
                painter.drawRect(rect)
                painter.drawText(rect, Qt.AlignCenter,str(row[1])+"-"+str(row[2])+" ("+str(row[2]-row[1]+1)+")")
                xseek=xseek+colWidth
                rect.setRect(xseek,yseek,colWidth,rowWidth)
                painter.drawRect(rect)
                painter.drawText(rect, Qt.AlignCenter,row[3])
                xseek=oxseek
                yseek=yseek+rowWidth
            painter.end()

    def exportAsCsv(self):
        if self.doArrangment()==0:
            return 0
        fileName = QFileDialog.getSaveFileName(self, "Save File","untitled.csv","*.csv")
        fp=open(fileName,'w')

        #print room allocations
        for room in  self.roomAllocation:
            fp.writelines('"'+room[0]+'"'+"\n")
            #find the largest column
            largest=0
            fp.writelines('"",')
            for i in range(0,len(room[1])):
                fp.writelines('"'+self.rTitle[i]+'",')
            fp.writelines("\n")
            for row in room[1]:
                if len(row)>largest:
                    largest=len(row)

            for i in range(0,largest):
                fp.writelines('"'+str((i+1))+'",')
                for col in room[1]:
                    if i <len(col):
                        if col[i]=='EM':
                            fp.writelines('"-",')
                        else:
                            fp.writelines('"'+col[i][0]+"-"+str(col[i][1])+'",')

                    else:
                        fp.writelines('"",')
                fp.writelines("\n")
            fp.writelines("\n")

        #print summary reports
        fp.writelines('"Summary of room allocation"\n')
        fp.writelines('"Branch","from","To","Room"\n')
        for row in self.rSummary:
            fp.writelines('"'+row[0]+'","'+str(row[1])+'","'+str(row[2])+'","'+row[3]+'"\n')
        fp.close()

    def createStudList(self):
        slist=[]
        sslist=[]
        if self.shuffle==0 or self.shuffle==1:
            for i in range(0,self.studTable.rowCount()):
                className=self.getTableData(self.studTable,i,0)
                sfrom=self.getTableData(self.studTable,i,1)
                to=self.getTableData(self.studTable,i,2)
                if className=='EMPTY' or sfrom=='EMPTY':
                    if debug==1:
                        print "Class Name and from field are mandatory" #Make its as msg box
                    return
                if to=='EMPTY':
                    to=sfrom
                for j in range(int(sfrom),int(to)+1):
                    slist.append([str(className),j,i])
            if rev_stud_list==1 and self.shuffle==1:
                if len(slist)%2==0:
                    fw_max=len(slist)/2
                    bwd_max=len(slist)/2
                else:
                    fw_max=len(slist)/2+1
                    bwd_max=len(slist)/2
    
                fwlist=slist[0:fw_max]
                bwlist=slist[fw_max:]
                bwlist.reverse()
                slist=fwlist
                slist.extend(bwlist)
        if self.shuffle==1:
            if debug==1:
                print "Shuffle is checked"
                

        return slist

    def createRoom(self,seatTableRow):
        room=[]
        size=0
        for j in range(1,columnMax):
            if self.getTableData(self.seatTable,seatTableRow,j)=='EMPTY':
                    continue
            else:
                room.append(range(1,int(self.getTableData(self.seatTable,seatTableRow,j))+1))
        for j in range(0,len(room)):
            size=size+len(room[j])
        return (size,room)


app = QApplication(sys.argv)
widget=Gui()
widget.show()
sys.exit(app.exec_())
