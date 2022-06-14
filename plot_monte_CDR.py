# from matplotlib.lines import _LineStyle
from math import ceil
from matplotlib.axis import XAxis
import matplotlib.pyplot as plt
import numpy as np
import csv
from os.path import exists    
from matplotlib import cm

def Plot_Data(filename,xparms,yparms,disc,titlein,count,pay_ind):
    rows=[]
    inpy2=[]
    inpx2=[]
    fig = plt.figure(figsize=plt.figaspect(0.5))
    if exists(filename):
        with open(filename, 'r') as file:
            csvreader = csv.reader(file)
            header = next(csvreader)
            for row in csvreader:
                inp=(row[0][:].split(' '))
                inp = ([float(x) for x in inp])

                
                inpy=[]
                inpx=[]
                if inp[0]==1:
                    inpy.append(1)
                    payw=inp[pay_ind]
                else:
                    inpy.append(0)
                for j in yparms:
                    if len(inp)>j:
                        inpy.append(inp[j])
                    else:
                        inpy.append(0)
                for j in xparms:
                    if len(inp)>j:
                        inpx.append(inp[j])
                    else:
                        inpx.append(0)
                inpy2.append(inpy)
                inpx2.append(inpx)
                rows.append(row)
        inpy=np.array(inpy2)
        inpx=np.array(inpx2)
    for i in range(len(xparms)):
        
        plt.figure(i+count)
        plt.suptitle(titlein+' '+str(payw)+' kg')
        for j in range(len(yparms)):
            
            
            
            plt.subplot(len(yparms)/2, len(yparms)/2, j+1)
            for k in range(len(inpx[:,0])):
                if inpy[k,0]==1:
                    plt.plot(inpx[k,i],inpy[k,j+1],'b.')
                    # if inpx[k,0]==3:
                    #     plt.plot(inpx[k,i],inpy[k,j+1],'b.')
                    # elif inpx[k,0]==4:
                    #     plt.plot(inpx[k,i],inpy[k,j+1],'r.')
                    # else:
                    #     plt.plot(inpx[k,i],inpy[k,j+1],'g.')
                else:
                    plt.plot(inpx[k,i],inpy[k,j+1],'r.')

            plt.xlabel(disc[xparms[i]-1])
            plt.ylabel(disc[yparms[j]-1])
        
def Plot_Stable_Area(filename,xparms,yparms,disc,titlein,count,pay_ind):
    rows=[]
    inpy2=[]
    inpx2=[]
    fig = plt.figure(figsize=plt.figaspect(0.5))
    if exists(filename):
        with open(filename, 'r') as file:
            csvreader = csv.reader(file)
            header = next(csvreader)
            for row in csvreader:
                inp=(row[0][:].split(' '))
                inp = ([float(x) for x in inp])
                payw=inp[pay_ind]
                inpy=[]
                inpx=[]
                if inp[0]==1:
                    inpy.append(1)
                else:
                    inpy.append(0)
                for j in yparms:
                    if len(inp)>j:
                        inpy.append(inp[j])
                    else:
                        inpy.append(0)
                for j in xparms:
                    inpx.append(inp[j])
                inpy2.append(inpy)
                inpx2.append(inpx)
                rows.append(row)
        inpy=np.array(inpy2)
        inpx=np.array(inpx2)
    for i in range(len(xparms)):
        
        plt.figure(i+count)
        plt.suptitle('Vehicle Weight '+str(payw*2.20462)+' lbs')
        for j in range(len(yparms)):
            
            
            if len(yparms)==2:
                plt.subplot(2, 1, j+1)
            elif len(yparms)==1:
                plt.subplot(1, 1, j+1)
            else:
                plt.subplot(len(yparms)/2, len(yparms)/2, j+1)
            for k in range(len(inpx[:,0])):
                if inpy[k,0]==1:
                    plt.plot(inpx[k,i],inpy[k,j+1],'b.')
                    # plt.plot(inpx[k,i]*39.3701,inpy[k,j+1]*39.3701,'b.')
                    # if inpx[k,0]==3:
                    #     plt.plot(inpx[k,i],inpy[k,j+1],'b.')
                    # elif inpx[k,0]==4:
                    #     plt.plot(inpx[k,i],inpy[k,j+1],'r.')
                    # else:
                    #     plt.plot(inpx[k,i],inpy[k,j+1],'g.')
                else:
                    # plt.plot(inpx[k,i]*39.3701,inpy[k,j+1]*39.3701,'r.')
                    plt.plot(inpx[k,i],inpy[k,j+1],'r.')

            plt.xlabel(disc[xparms[i]-1])
            plt.ylabel(disc[yparms[j]-1])

def Load_Data(path,filenamelist,pay_ind,rows):
    rows=[]
    inpy2=[]
    inpx2=[]
    leninp=0
    # fig = plt.figure(figsize=plt.figaspect(0.5))
    for i in filenamelist:
        filename=path+i
        if exists(filename):
            with open(filename, 'r') as file:
                csvreader = csv.reader(file)
                header = next(csvreader)
                coun=0
                for row in csvreader:
                    # print(coun)
                    # coun=coun+1
                    inp=(row[0][:].split(' '))
                    inp = ([float(x) for x in inp])
                    if inp[1]==0:
                        inp[10:11]=[]
                        inp[1:3]=[]
                    payw=inp[pay_ind]
                    if inp[0]==1:
                        leninp=len(inp)
                        rows=np.append(rows,np.array(inp))
                    else:
                        if leninp!=0:
                            zer=np.zeros(leninp-len(inp))
                            inp=np.append(inp,zer)
                            rows=np.append(rows,np.array(inp))
    return np.reshape(rows,(-1,leninp))

def friction_plot(path,filenamelist,pay_ind):
    frictionin=np.linspace(0.1,0.5,10)
    count=0
    fig = plt.figure(figsize=(12, 6))
    for i in filenamelist:
        filename=path+i
        if exists(filename):
            with open(filename, 'r') as file:
                csvreader = csv.reader(file)
                header = next(csvreader)
                for row in csvreader:
                    inp=(row[0][:].split(' '))
                    inp = ([float(x) for x in inp])
                    payw=inp[pay_ind]
                    if inp[0]==1:    
                        plt.plot(int(inp[pay_ind]*2.20462),frictionin[count],'b.',markersize=20)
                    else:
                        plt.plot(int(inp[pay_ind]*2.20462),frictionin[count],'r.',markersize=20)
                    count=count+1
                    if count==len(frictionin):
                        count=0
        fs = 24
        plt.tight_layout()
        plt.xlabel('Vehicle Weight [lbs]',fontsize=fs)
        plt.ylabel('Friction Coefficient',fontsize=fs)
        plt.tick_params(axis='x', labelsize=fs)
        plt.tick_params(axis='y', labelsize=fs)        

def Weight_plots(data,xparm,yparm,names,count):
    
    plt.figure(count)
    for i in range(len(data[:,0])):
        if data[i,0]==1:
            plt.plot(data[i,xparm],data[i,yparm],'b.')
        # else:
        #     plt.plot(data[i][xparm],data[i][yparm],'r.')
    # plt.suptitle(titlein+' '+str(payw)+' kg')
    plt.xlabel(disc[xparm-1])
    plt.ylabel(disc[yparm-1])

def Plot_tvp(data,xind,yind,payloadind):
    pay=np.unique(data[:,payloadind])
    colors=['.b','.r','.g','.k']
    # for i in range(len(data[:,0])):

    #     plt.plot(data[i,xind],data[i,yind])
    for k in range(len(pay)):
        xval=[]
        yval=[]
        for i in range(len(data[:,0])):
            if data[i,payloadind]==pay[k]:
                xval.append(data[i,xind])
                yval.append(data[i,yind])
        plt.plot(xval,yval,colors[k])
        plt.xlabel('Torque [Nm]')
        plt.ylabel('Average Power [W]')

def Plot_tvr(data,xind,yind,payloadind,sty):
    pay=np.unique(data[:,payloadind])
    colors=['b','r','g','k']
    fig = plt.figure(figsize=(12, 6))
    # for i in range(len(data[:,0])):
    fs=26
    # for i in range(len(data[:,0])):

    #     plt.plot(data[i,xind],data[i,yind])
    for k in range(len(pay)):
        xval=[]
        yval=[]
        for i in range(len(data[:,0])):
            if data[i,payloadind]==pay[k]:
                xval.append(data[i,xind]*39.37/6.85)
                yval.append(max(data[i,yind:])*0.73756214927727)
        plt.plot(xval,yval,colors[k]+sty,linewidth=5)
        plt.xlim([.5, 1.75])
        plt.ylim([30, 150])
        plt.xlabel('Radius/Step Rise',fontsize=fs)
        plt.ylabel('Torque [lbs-ft]',fontsize=fs)
        plt.tick_params(axis='x', labelsize=fs)
        plt.tick_params(axis='y', labelsize=fs)
        plt.tight_layout()
        plt.legend(['Weight = '+str(int(pay[0]*2.20462))+' lbs', 'Weight = '+str(int(pay[1]*2.20462))+' lbs','Weight = '+str(int(pay[2]*2.20462))+' lbs','Weight = '+str(int(pay[3]*2.20462))+' lbs'],fontsize=fs)

def Plot_svr(data,xind,yind,payloadind,sty):
    pay=np.unique(data[:,payloadind])
    colors=['b','r','g','k']
    fig = plt.figure(figsize=(12, 6))
    # for i in range(len(data[:,0])):
    fs=26    
    # for i in range(len(data[:,0])):

    #     plt.plot(data[i,xind],data[i,yind])
    for k in range(len(pay)):
        xval=[]
        yval=[]
        for i in range(len(data[:,0])):
            if data[i,payloadind]==pay[k]:
                xval.append(data[i,xind]*39.37/6.85)
                yval.append((data[i,yind]*11/10))
        plt.plot(xval,yval,colors[k]+sty,linewidth=3)
        plt.xlim([.5, 1.75])
        # plt.ylim([30, 120])
        plt.tight_layout()
        plt.xlabel('Radius/Step Rise',fontsize=fs)

        plt.ylabel('Speed [step/min]',fontsize=fs)
        plt.tick_params(axis='x', labelsize=fs)
        plt.tick_params(axis='y', labelsize=fs)
        plt.legend(['Weight = '+str(int(pay[0]*2.20462))+' lbs', 'Weight = '+str(int(pay[1]*2.20462))+' lbs','Weight = '+str(int(pay[2]*2.20462))+' lbs','Weight = '+str(int(pay[3]*2.20462))+' lbs'],fontsize=fs)

def Plot_svt(data,xind,yind,payloadind,sty):
    pay=np.unique(data[:,payloadind])
    colors=['b','r','g','k']
    # for i in range(len(data[:,0])):

    #     plt.plot(data[i,xind],data[i,yind])
    for k in range(len(pay)):
        xval=[]
        yval=[]
        for i in range(len(data[:,0])):
            if data[i,payloadind]==pay[k]:
                xval.append(data[i,xind]*0.73756214927727)
                yval.append((data[i,yind]*11/10))
        plt.plot(xval,yval,colors[k]+sty,linewidth=3)
        # plt.xlim([.5, 1.75])
        # plt.ylim([30, 120])
        plt.xlabel('Radius/Step Rise',fontsize=14)
        plt.ylabel('Speed [step/min]',fontsize=14)
        plt.tick_params(axis='x', labelsize=14)
        plt.tick_params(axis='y', labelsize=14)
        plt.legend(['Weight = '+str(int(pay[0]*2.20462))+' lbs', 'Weight = '+str(int(pay[1]*2.20462))+' lbs','Weight = '+str(int(pay[2]*2.20462))+' lbs','Weight = '+str(int(pay[3]*2.20462))+' lbs'],fontsize=14)

def Plot_pvr(data,xind,yind,payloadind,sty):
    pay=np.unique(data[:,payloadind])
    colors=['b','r','g','k']
    ideal_p=(6.85)/39.37*pay*9.81
    fig = plt.figure(figsize=(12, 6))
    # for i in range(len(data[:,0])):
    fs=26
    #     plt.plot(data[i,xind],data[i,yind])
    for k in range(len(pay)):
        xval=[]
        yval=[]
        for i in range(len(data[:,0])):
            if data[i,payloadind]==pay[k]:
                xval.append(data[i,xind]*39.37/6.85)
                yval.append((data[i,yind]*4))
        plt.plot(xval,yval,colors[k]+sty,linewidth=5)
        
        plt.xlim([.5, 1.75])
        plt.ylim([50, 800])
        plt.tight_layout()
        plt.xlabel('Radius/Step Rise',fontsize=fs)
        plt.ylabel('Power [W]',fontsize=fs)
        plt.tick_params(axis='x', labelsize=fs)
        plt.tick_params(axis='y', labelsize=fs)
        plt.legend(['Weight = '+str(int(pay[0]*2.20462))+' lbs', 'Weight = '+str(int(pay[1]*2.20462))+' lbs','Weight = '+str(int(pay[2]*2.20462))+' lbs','Weight = '+str(int(pay[3]*2.20462))+' lbs'],fontsize=fs)
    for k in range(len(pay)):
        # ideal_p=(6.85)/39.37*pay[k]
        plt.plot([0,2],[ideal_p[k],ideal_p[k]],colors[k]+'--')

def Plot_Scatters(data,xind,yind,disc):
    MS=10.
    for ii in range(len(yind)):
        plt.figure(ii)
        success=np.reshape(np.where(data[:,0]==1),(-1))
        fail=np.reshape(np.where(data[:,0]==0),(-1))
        plt.plot(data[success[:],xind],data[success[:],yind[ii]],'.b',markersize=MS)
        plt.plot(data[fail[:],xind],data[fail[:],yind[ii]],'.r',markersize=MS)
        plt.xlabel(disc[xind-1])
        plt.ylabel(disc[yind[ii]-1]) 

def Plot_Scatters_Bins(data,xind,yind,disc,bin):
    MS=10.
    binrange=np.linspace(min(data[:,bin])-0.01,max(data[:,bin])+0.01,5)
    for jj in range(1,len(binrange)):
        plt.figure(jj)

        passp=[]
        failp=[]
        for ii in range(len(data[:,0])):
            # if jj == len(binrange)-1:
            if data[ii,0]==1 and data[ii,bin]>=binrange[jj-1] and data[ii,bin]<binrange[jj]:
                passp.append(ii)
            elif data[ii,0]==0 and data[ii,bin]>=binrange[jj-1] and data[ii,bin]<binrange[jj]:
                failp.append(ii)

        plt.plot(data[passp,xind],data[passp,yind],'.b')
        plt.plot(data[failp,xind],data[failp,yind],'.r')
        plt.xlabel(disc[xind-1])
        plt.ylabel(disc[yind-1])
        plt.title(binrange[jj])

def Plot_Scatters_Bins_Rad(data,xind,yind,disc,bin,radind,c):
    MS=10.
    binrange=np.linspace(min(data[:,bin])-0.01,max(data[:,bin])+0.01,5)
    for jj in range(1,len(binrange)):
        plt.figure(jj)

        passpl=[]
        failpl=[]
        passpu=[]
        failpu=[]
        for ii in range(len(data[:,0])):
            # if jj == len(binrange)-1:
            if data[ii,0]==1 and data[ii,bin]>=binrange[jj-1] and data[ii,bin]<binrange[jj]:
                if data[ii,radind]<c:
                    passpl.append(ii)
                else:
                    passpu.append(ii)
            elif data[ii,0]==0 and data[ii,bin]>=binrange[jj-1] and data[ii,bin]<binrange[jj]:
                if data[ii,radind]<c:
                    failpl.append(ii)
                else:
                    failpu.append(ii)

        plt.plot(data[passpl,xind],data[passpl,yind],'.b')
        # plt.plot(data[failpl,xind],data[failpl,yind],'.r')
        plt.plot(data[passpu,xind],data[passpu,yind],'.g')
        # plt.plot(data[failpl,xind],data[failpl,yind],'.r')
        plt.xlabel(disc[xind-1])
        plt.ylabel(disc[yind-1])
        plt.title(binrange[jj])

def Plot_Heat(data,xind,yind,disc,bin,nameo):
      
    MS=10.
    binrange=np.linspace(min(data[:,bin])-0.01,max(data[:,bin])+0.01,5)
    for jj in range(1,len(binrange)):
        plt.figure(jj)
        
        # x = np.linspace(min(data[:,xind])-0.0001, max(data[:,xind])+0.0001, 10)
        # y = np.linspace(min(data[:,yind])-0.0001, max(data[:,yind])+0.0001, 10)
        fpts=3
        x = np.concatenate((np.linspace(min(data[:,xind])-0.0001, max(data[:,xind])-3, 14),np.linspace(max(data[:,xind])-3+3/(fpts-1),max(data[:,xind])+0.001, fpts)))
        y = np.concatenate((np.linspace(min(data[:,yind])-0.0001, max(data[:,yind])-3, 14),np.linspace(max(data[:,yind])-3+3/(fpts-1),max(data[:,yind])+0.001, fpts)))
        # x.append(x,np.linspace(max(data[:,xind])-3,max(data[:,xind])+0.001, 10))
        # y.append(y,np.linspace(max(data[:,yind])-3,max(data[:,yind])+0.001, 10))
        # full coorindate arrays
        xx, yy = np.meshgrid(x, y)
        zzp = np.zeros(np.shape(xx))
        zzf = np.zeros(np.shape(xx))
        passp=[]
        failp=[]
        cf=0
        for ii in range(len(data[:,0])):
            # if jj == len(binrange)-1:
            if data[ii,0]==1 and data[ii,bin]>=binrange[jj-1] and data[ii,bin]<binrange[jj]:
                for kk in range(len(xx[0,:])-1):
                    # if data[ii,xind]>xx[0,-2] and data[ii,yind]>yy[-2,0]:

                    if data[ii,xind]>xx[0,kk] and data[ii,xind]<xx[0,kk+1]:
                        for hh in range(len(yy[:,0])-1):
                            if data[ii,yind]>yy[hh,0] and data[ii,yind]<yy[hh+1,0]:
                                zzp[hh,kk]=zzp[hh,kk]+1
                               
                passp.append(ii)
            elif data[ii,0]==0 and data[ii,bin]>=binrange[jj-1] and data[ii,bin]<binrange[jj]:
                for kk in range(len(xx[0,:])-1):
                    if data[ii,xind]>xx[0,kk] and data[ii,xind]<xx[0,kk+1]:
                        for hh in range(len(yy[:,0])-1):
                            if data[ii,yind]>yy[hh,0] and data[ii,yind]<yy[hh+1,0]:
                                zzf[hh,kk]=zzf[hh,kk]+1
                               
                failp.append(ii)

        zz=zzp/(zzp+zzf)
        for ii in range(len(zz[:,0])):
            for hh in range(len(zz[0,:])):
                if np.isnan(zz[ii,hh])==True:
                    zz[ii,hh]=0
                    count=0
                    for ki in range(3):
                        for kj in range(3):
                            if ii+ki<len(zz[0,:]) and hh+kj<len(zz[:,0]):
                                if np.isnan(zz[ii+ki,hh+kj])==False:
                                    zz[ii,hh]=zz[ii,hh]+zz[ii+ki,hh+kj]
                                    count=count+1
                    if count>0:
                        zz[ii,hh]=zz[ii,hh]/count

                    
        cs = plt.contourf(xx[0:-1,0:-1],yy[0:-1,0:-1],zz[0:-1,0:-1],levels=np.linspace(0,1,11))    
        # plt.plot(data[passp,xind],data[passp,yind],'.b')
        # plt.plot(data[failp,xind],data[failp,yind],'.r')   
        # for i in range(len(x)):
        #     # for j in range(len(y)-1):
        #     plt.plot([x[i],x[i]],[y[0],y[-1]],'k')
        #     plt.plot([x[0],x[-1]],[y[i],y[i]],'k')
        cbar = plt.colorbar(cs)
        # x = 
        # y = [-8, -4, 0, 4]
        # default_x_ticks = range(len(x))
        # plt.yticks(default_x_ticks, y)
        plt.yticks([-7.5, -4 , -0.5, 3.0], [-7.5, -4 , -0.5, 3])
        plt.xticks([-7.5, 0, 7.5, 15.], [-7.5, 0, 7.5, 15])
        plt.xlim([-7.5,15])
        plt.ylim([-7.75,3.0])
        plt.xlabel('CoM x pos [in]')#disc[xind-1])
        plt.ylabel('CoM z pos [in]')#disc[yind-1])
        # title="Wheel radius is between %s and %s inches" % (ceil(binrange[jj-1]), ceil(binrange[jj]))
        title=" %s\" < r < %s\" " % (ceil(binrange[jj-1]), ceil(binrange[jj]))
        plt.title(title)
        plt.savefig(nameo+str(ceil(binrange[jj-1]))+'.pdf',bbox_inches='tight',dpi=200)

def Plot_Ave_Heat(data,xind,yind,disc,bin,data2):
    MS=10.
    binrange=np.linspace(min(data[:,bin])-0.01,max(data[:,bin])+0.01,5)
    for jj in range(1,len(binrange)):
        plt.figure(jj)
        xx, yy, zz1 = Get_Mesh(xind,yind,jj,binrange,data2,bin)
        xx, yy, zz2 = Get_Mesh(xind,yind,jj,binrange,data,bin)
        # x = np.linspace(min(data[:,xind])-0.0001, max(data[:,xind])+0.0001, 12)
        # y = np.linspace(min(data[:,yind])-0.0001, max(data[:,yind])+0.0001, 12)
        # # full coorindate arrays
        # xx, yy = np.meshgrid(x, y)
        # zzp = np.zeros(np.shape(xx))
        # zzf = np.zeros(np.shape(xx))
        # passp=[]
        # failp=[]
        # cf=0
        # for ii in range(len(data[:,0])):
        #     # if jj == len(binrange)-1:
        #     if data[ii,0]==1 and data[ii,bin]>=binrange[jj-1] and data[ii,bin]<binrange[jj]:
        #         for kk in range(len(xx[0,:])-1):
        #             # if data[ii,xind]>xx[0,-2] and data[ii,yind]>yy[-2,0]:

        #             if data[ii,xind]>xx[0,kk] and data[ii,xind]<xx[0,kk+1]:
        #                 for hh in range(len(yy[:,0])-1):
        #                     if data[ii,yind]>yy[hh,0] and data[ii,yind]<yy[hh+1,0]:
        #                         zzp[hh,kk]=zzp[hh,kk]+data
                               
        #         passp.append(ii)
        #     elif data[ii,0]==0 and data[ii,bin]>=binrange[jj-1] and data[ii,bin]<binrange[jj]:
        #         for kk in range(len(xx[0,:])-1):
        #             if data[ii,xind]>xx[0,kk] and data[ii,xind]<xx[0,kk+1]:
        #                 for hh in range(len(yy[:,0])-1):
        #                     if data[ii,yind]>yy[hh,0] and data[ii,yind]<yy[hh+1,0]:
        #                         zzf[hh,kk]=zzf[hh,kk]+1

        #         failp.append(ii)

        # zz=zzp/(zzp+zzf)
        cs = plt.contourf(xx[0:-1,0:-1],yy[0:-1,0:-1],zz1[0:-1,0:-1]-zz2[0:-1,0:-1],levels=np.linspace(0,1,11))
        # plt.plot(data[passp,xind],data[passp,yind],'.b')
        # plt.plot(data[failp,xind],data[failp,yind],'.r')
        # for i in range(len(x)):
        #     # for j in range(len(y)-1):
        #     plt.plot([x[i],x[i]],[y[0],y[-1]],'k')
        #     plt.plot([x[0],x[-1]],[y[i],y[i]],'k')
        cbar = plt.colorbar(cs)
        plt.xlabel(disc[xind-1])
        plt.ylabel(disc[yind-1])
        title="Wheel radius is between %s and %s inches" % (ceil(binrange[jj-1]), ceil(binrange[jj]))
        plt.title(title)

def Get_Mesh(xind,yind,jj,binrange,data,bin):
        x = np.linspace(min(data[:,xind])-0.0001, max(data[:,xind])+0.0001, 12)
        y = np.linspace(min(data[:,yind])-0.0001, max(data[:,yind])+0.0001, 12)
        # full coorindate arrays
        xx, yy = np.meshgrid(x, y)
        zzp = np.zeros(np.shape(xx))
        zzf = np.zeros(np.shape(xx))
        passp=[]
        failp=[]
        cf=0
        for ii in range(len(data[:,0])):
            # if jj == len(binrange)-1:
            if data[ii,0]==1 and data[ii,bin]>=binrange[jj-1] and data[ii,bin]<binrange[jj]:
                for kk in range(len(xx[0,:])-1):
                    # if data[ii,xind]>xx[0,-2] and data[ii,yind]>yy[-2,0]:

                    if data[ii,xind]>xx[0,kk] and data[ii,xind]<xx[0,kk+1]:
                        for hh in range(len(yy[:,0])-1):
                            if data[ii,yind]>yy[hh,0] and data[ii,yind]<yy[hh+1,0]:
                                zzp[hh,kk]=zzp[hh,kk]+1
                               
                passp.append(ii)
            elif data[ii,0]==0 and data[ii,bin]>=binrange[jj-1] and data[ii,bin]<binrange[jj]:
                for kk in range(len(xx[0,:])-1):
                    if data[ii,xind]>xx[0,kk] and data[ii,xind]<xx[0,kk+1]:
                        for hh in range(len(yy[:,0])-1):
                            if data[ii,yind]>yy[hh,0] and data[ii,yind]<yy[hh+1,0]:
                                zzf[hh,kk]=zzf[hh,kk]+1
                               
                failp.append(ii)

        zz=zzp/(zzp+zzf)    
        return xx, yy, zz
    ## split grid ##
#plt.rcParams.keys() gives all inputs
font = {'font.serif' : 'Times New Toman',
        'font.size'   : 28}
plt.rcParams.update(font)
## for wheeled ##
# 1 : radius    2 : wheelbase   3 : payloadx  4 : payloadz   5 : step_rise    6 : step_slope    7 : payload_weight
# 8 : sim time    9 : speed [steps/min]  10 : mass  11 : max power  12 : average power   13 : power sum  14-end : max torque 
disc=['radius','wheelbase','payloadx','payloadz','step_rise','step_slope','payload_weight','sim_time','speed','mass','max power','average power','power sum','max torque']
path = 'Wheel_CDR35'
# filenamelist=['payxlocVzloc_pay60.csv']
filenamelist=['payxlocVzloc_pay0.csv','payxlocVzloc_pay20.csv','payxlocVzloc_pay40.csv','payxlocVzloc_pay60.csv']
data=Load_Data(path,filenamelist,7,[])
for i in range(len(data[:,0])):
    if data[i,2]==0:
        data[i,1:]=data[i,3:-3]

data[:,1:6]=data[:,1:6]*39.3701
# path = 'Wheel_CDR35v2'
# data2=Load_Data(path,filenamelist,7,[])
# data2[:,1:6]=data2[:,1:6]*39.3701


# Plot_Ave_Heat(data,3,4,disc,1,data2)
# Plot_Scatters(data,3,[4,1],disc)
# Plot_Scatters_Bins(data,3,4,disc,7)
# Plot_Scatters_Bins(data,3,4,disc,7)
Plot_Heat(data,3,4,disc,1,path)
plt.show()

## for planetary dolly ##
# 1 : sub_radius    2 : wheel_num       3 : radius      4 : wheelbase           5 : payloadx    6 : payloadz    7 : step_rise
# 8 : step_slope    9 : payload_weight  10 : sim time   11 : speed [steps/min]  12 : mass       13 : max power
# 14: average power 15: power sum       16-end : max torque 
# disc=['sub_rad','num_wheel','radius','wheelbase','paylocx','paylocz','step_rise','step_slope','pay_weight','sim time','speed','mass','max power','average power','power sum','max torque']
# path = 'Planet_CDR35'
# filenamelist=['payxlocVzloc_pay0.csv','payxlocVzloc_pay20.csv','payxlocVzloc_pay40.csv','payxlocVzloc_pay60.csv']
# data=Load_Data(path,filenamelist,9,[])
# data[:,3:9]=data[:,3:9]*39.3701
# # path = 'Planet_CDR35'
# # data2=Load_Data(path,filenamelist,9,[])
# # data2[:,3:9]=data2[:,3:9]*39.3701
# # Plot_Scatters(data,5,[14,6],disc)
# # Plot_Scatters_Bins(data,5,6,disc,3)
# # Plot_Scatters_Bins_Rad(data,5,6,disc,9,3,9)
# Plot_Heat(data,5,6,disc,3,path)
# # Plot_Ave_Heat(data,5,6,disc,3,data2)
# plt.show()