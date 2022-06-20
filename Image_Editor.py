'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Python cImage Editor v0.4.0 beta
 by Alessandro De Marco
Features:                                                              '''
#1 Crop, #2 Rotate, #3 Flip, #4 Enlarge X2, #5 Adjust brightness,
#6 Adjust contrast, #7 Adjust saturation, #8 Grayscale, #9 Sepia,
#10 Inverted colors, #11 Solarize, #12 Posterize, #13 "Noisize",
#14 Pseudo HDR, #15 Color shift, #16 Show histograms.
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#1 Crop
def crop(img,win):
    c=win.captureClicks(2)
    (x1,y1)=c[0]
    (x2,y2)=c[1]
    if x1>x2 and y2>y1:
        (x2,y1)=c[0]
        (x1,y2)=c[1]
    elif x2>x1 and y1>y2:
        (x1,y2)=c[0]
        (x2,y1)=c[1]
    elif x1>x2 and y1>y2:
        (x2,y2)=c[0]
        (x1,y1)=c[1]
    elif x1==x2 or y1==y2:
        (x1,y1)=(0,0)
        (x2,y2)=(1,1)
    print("Processing...")
    new_img=image.EmptyImage(x2-x1,y2-y1)
    for i in range(y1,y2):
        for j in range(x1,x2):
            p=img.getPixel(j,i)
            new_img.setPixel(j-x1,i-y1,p)
    return new_img

#2 Rotate
def rotate(img,direction):
    w=img.getWidth()
    h=img.getHeight()
    new_img=image.EmptyImage(h,w)
    if direction=="l":  #left
        print("Processing...")
        for i in range(h):
            for j in range(w):
                p=img.getPixel(j,i)
                new_img.setPixel(i,w-j-1,p)
        return new_img
    elif direction=="r":  #right
        print("Processing...")
        for i in range(h):
            for j in range(w):
                p=img.getPixel(j,i)
                new_img.setPixel(h-i-1,j,p)
        return new_img
    
#3 Flip
def flip(img,axis):
    w=img.getWidth()
    h=img.getHeight()
    new_img=image.EmptyImage(w,h)
    if axis=="1":  #horizontal
        print("Processing...")
        for i in range(h):
            for j in range(w):
                p=img.getPixel(j,i)
                new_img.setPixel(w-j-1,i,p)
        return new_img
    elif axis=="2":  #vertical
        print("Processing...")
        for i in range(h):
            for j in range(w):
                p=img.getPixel(j,i)
                new_img.setPixel(j,h-i-1,p)
        return new_img

#4 Enlarge
def enlarge(img):
    w=img.getWidth()
    h=img.getHeight()
    new_img=image.EmptyImage(w*2,h*2)
    for i in range(h):
        for j in range(w):
            p=img.getPixel(j,i)
            new_img.setPixel(j*2,i*2,p)
            new_img.setPixel(j*2+1,i*2,p)
            new_img.setPixel(j*2,i*2+1,p)
            new_img.setPixel(j*2+1,i*2+1,p)
    return new_img

#5 Brightness
def truncate(value):  # truncates values above 255 and below 0
    if value<0:
        value=0
    elif value>255:
        value=255
    return value

def brightness(img,brightness):
    for j in range(img.getWidth()):
        for i in range(img.getHeight()):
            p=img.getPixel(j,i)
            newRed=truncate(p.getRed()+brightness)
            newGreen=truncate(p.getGreen()+brightness)
            newBlue=truncate(p.getBlue()+brightness)
            newPixel=image.Pixel(newRed,newGreen,newBlue)
            img.setPixel(j,i,newPixel)
    return img

#6 Contrast
def contrast(img,contrast):
    for j in range(img.getWidth()):
        for i in range(img.getHeight()):
            p=img.getPixel(j,i)
            factor=(259*(contrast+255))/(255*(259-contrast))
            newRed=int(round(truncate(factor*(p.getRed()-128)+128)))
            newGreen=int(round(truncate(factor*(p.getGreen()-128)+128)))
            newBlue=int(round(truncate(factor*(p.getBlue()-128)+128)))
            newPixel=image.Pixel(newRed,newGreen,newBlue)
            img.setPixel(j,i,newPixel)
    return img

#7 Saturation
def maxi(l):  # finds the maximum value of a list
    ma=l[0]
    for i in range(1,len(l)):
        if l[i]>ma:
            ma=l[i]
    return ma

def mini(l):  # finds the minimum value of a list
    mi=l[0]
    for i in range(1,len(l)):
        if l[i]<mi:
            mi=l[i]
    return mi

def saturation_percentage(value,add):  # calculates the S value in relation to the added/subtracted value
    value*=100
    value+=add
    value/=100
    if value<=0:
        value=0.00000001
    elif value>100:
        value=100
    return value

def RGBtoHSLtoRGB(img,add):
    for i in range(img.getHeight()):
        for j in range(img.getWidth()):
            p=img.getPixel(j,i)
            R=p.getRed()/255
            G=p.getGreen()/255
            B=p.getBlue()/255
            RGB=[R,G,B]
            maxv=maxi(RGB)
            minv=mini(RGB)
            L=(minv+maxv)/2
            if minv==maxv:
                S=0
                H=0
            else:
                if L<0.5:
                    S=(maxv-minv)/(maxv+minv)
                else:
                    S=(maxv-minv)/(2.0-maxv-minv)
                if R==maxv:
                    H=(G-B)/(maxv-minv)
                elif G==maxv:
                    H=2.0+(B-R)/(maxv-minv)
                else:
                    H=4.0+(R-G)/(maxv-minv)
            H*=60
            if H<0:
                H+=360
            S=saturation_percentage(S,add)
            #
            rR=gG=bB=0
            if S==0:
                rR=gG=bB=L*255
            else:
                if L<0.5:
                    temp_1=L*(1.0+S)
                else:
                    temp_1=L+S-L*S
                temp_2=2*L-temp_1
                H/=360
                temp_R=H+0.333
                temp_G=H
                temp_B=H-0.333
                temp_R=check_temp(temp_R)
                temp_G=check_temp(temp_G)
                temp_B=check_temp(temp_B)
                rR=check_temp_c(temp_R,rR,temp_1,temp_2)
                gG=check_temp_c(temp_G,gG,temp_1,temp_2)
                bB=check_temp_c(temp_B,bB,temp_1,temp_2)
                R=int(round(truncate(rR*255)))
                G=int(round(truncate(gG*255)))
                B=int(round(truncate(bB*255)))
                newPixel=image.Pixel(R,G,B)
                img.setPixel(j,i,newPixel)
    return img

def check_temp(temp):  # temporary values calc
    if temp<0:
        temp+=1
    elif temp>1:
        temp-=1
    return temp

def check_temp_c(temp_c,cC,temp_1,temp_2):  # temporary values calc
    if 6*temp_c<1:
        cC=temp_2+(temp_1-temp_2)*6*temp_c
    else:
        if 2*temp_c<1:
            cC=temp_1
        else:
            if 3*temp_c<2:
                cC=temp_2+(temp_1-temp_2)*(0.666-temp_c)*6
            else:
                cC=temp_2       
    return cC

#8 Grayscale
def grayscale(img):
    for i in range(img.getHeight()):
        for j in range(img.getWidth()):
            p=img.getPixel(j,i)
            avg=(p.getRed()+p.getGreen()+p.getBlue())//3
            newPixel=image.Pixel(avg,avg,avg)
            img.setPixel(j,i,newPixel)
    return img

#9 Sepia
def sepia(img):
    for i in range(img.getHeight()):
        for j in range(img.getWidth()):
            p=img.getPixel(j,i)
            R,G,B=p.getRed(),p.getGreen(),p.getBlue()
            newRed=int(round(truncate(R*0.393+G*0.769+B*0.189)))
            newGreen=int(round(truncate(R*0.349+G*0.686+B*0.168)))
            newBlue=int(round(truncate(R*0.272+G*0.534+B*0.131)))
            newPixel=image.Pixel(newRed,newGreen,newBlue)
            img.setPixel(j,i,newPixel)
    return img

#10 Inverted
def invert(img):
    for i in range(img.getHeight()):
        for j in range(img.getWidth()):
            p=img.getPixel(j,i)
            newRed=255-p.getRed()
            newGreen=255-p.getGreen()
            newBlue=255-p.getBlue()
            newPixel=image.Pixel(newRed,newGreen,newBlue)
            img.setPixel(j,i,newPixel)
    return img

#11 Solarization
def solarize(img):
    for i in range(img.getHeight()):
        for j in range(img.getWidth()):
            p=img.getPixel(j,i)
            R,G,B=p.getRed(),p.getGreen(),p.getBlue()
            intensity=(R+G+B)/3.0
            if intensity<80:  # treshold = 80
                newPixel=image.Pixel(255-R,255-G,255-B)
                img.setPixel(j,i,newPixel)
    return img

#12 Posterization
def ranges(c):
    if c in range(32):
        newc=0
    elif c in range(32,96):
        newc=64
    elif c in range(96,160):
        newc=128
    elif c in range(160,224):
        newc=192
    else:
        newc=255
    return newc

def posterize(img):
    for i in range(img.getHeight()):
        for j in range(img.getWidth()):
            p=img.getPixel(j,i)
            R,G,B=p.getRed(),p.getGreen(),p.getBlue()
            newRed=ranges(R)
            newGreen=ranges(G)
            newBlue=ranges(B)
            newPixel=image.Pixel(newRed,newGreen,newBlue)
            img.setPixel(j,i,newPixel)
    return img

#13 Noise
def noise(img):
    import math
    import random
    radius=15  # radius
    for i in range(img.getHeight()):
        for j in range(img.getWidth()):
            p=img.getPixel(j,i)
            R,G,B=p.getRed(),p.getGreen(),p.getBlue()
            mod=math.floor((random.randint(1,10)*radius)-50)
            R+=mod
            G+=mod
            B+=mod
            newPixel=image.Pixel(truncate(R),truncate(G),truncate(B))
            img.setPixel(j,i,newPixel)
    return img

def colorNoise(img):
    import random
    for i in range(img.getHeight()):
        for j in range(img.getWidth()):
            p=img.getPixel(j,i)
            colors=[0,p.getRed(),p.getGreen(),p.getBlue()]*2
            rindex=random.randint(0,7)
            gindex=random.randint(0,7)
            bindex=random.randint(0,7)
            R=colors[rindex]
            G=colors[gindex]
            B=colors[bindex]
            newPixel=image.Pixel(R,G,B)
            img.setPixel(j,i,newPixel)
    return img

#14 HDR
def RGBtoHSVtoRGB(img):
    import math
    n=img.getHeight()*img.getWidth()
    histo=[0]*256
    for i in range(img.getHeight()):
        for j in range(img.getWidth()):
            p=img.getPixel(j,i)
            R,G,B=p.getRed(),p.getGreen(),p.getBlue()
            avg=(R+G+B)//3
            histo[avg]+=1
            RGB=[R,G,B]
            maxv=maxi(RGB)
            minv=mini(RGB)
            V=maxv
            if minv==maxv:
                S=0
                H=0
            else:
                delta=maxv-minv
                S=delta/maxv
                Rv=(maxv-R)/delta
                Gv=(maxv-G)/delta
                Bv=(maxv-B)/delta
                if R==maxv:
                    H=Bv-Gv
                elif G==maxv:
                    H=2+Rv-Bv
                elif B==maxv:
                    H=4+Gv-Rv
                H*=60
                if H<0:
                    H+=360
            V=math.floor(255*(cdf(histo,V))/n)
            #
            rR=gG=bB=0
            if S==0.0:
                rR=gG=bB=V
            else:
                Chroma=S*V
                H/=60.0
                X=Chroma*(1.0-abs((H%2.0)-1.0))
                if H<1.0:
                    rR=Chroma
                    gG=X
                elif H<2.0:
                    rR=X
                    gG=Chroma
                elif H<3.0:
                    gG=Chroma
                    bB=X
                elif H<4.0:
                    gG=X
                    bB=Chroma
                elif H<5.0:
                    rR=X
                    bB=Chroma
                elif H<6.0:
                    rR=Chroma
                    bB=X
                minv=V-Chroma
                rR+=minv
                gG+=minv
                bB+=minv
            R=int(round(truncate(rR)))
            G=int(round(truncate(gG)))
            B=int(round(truncate(bB)))
            newPixel=image.Pixel(R,G,B)
            img.setPixel(j,i,newPixel)
    return img

def cdf(histo,V): #cumulative density function
    cd=0
    for i in range(V+1):
        cd+=histo[i]
    return cd

#15 Color shift '2^3*2^2*2^1 = 8*4*2 = 64 possible combinations between colors'
def recolor(img,choice):
    for i in range(img.getHeight()):
        for j in range(img.getWidth()):
            p=img.getPixel(j,i)
            R,G,B=p.getRed(),p.getGreen(),p.getBlue()
            if choice=="1":
                newPixel=image.Pixel(R,0,0)
            elif choice=="2":
                newPixel=image.Pixel(0,G,0)
            elif choice=="3":
                newPixel=image.Pixel(0,0,B)
            elif choice=="4":
                newPixel=image.Pixel(0,G,B)
            elif choice=="5":
                newPixel=image.Pixel(R,G,0)
            elif choice=="6":
                newPixel=image.Pixel(R,0,B)
            elif choice=="7":
                newPixel=image.Pixel(R,B,G)
            elif choice=="8":
                newPixel=image.Pixel(B,G,R)
            elif choice=="9":
                newPixel=image.Pixel(G,R,B)
            elif choice=="10":
                newPixel=image.Pixel(G,B,R)
            else:
                newPixel=image.Pixel(B,R,G)
            img.setPixel(j,i,newPixel)
    return img

def color_comp(index):
    if index==0:
        c="0"
    elif index==1 or index==4:
        c="R"
    elif index==2 or index==5:
        c="G"
    else:
        c="B"
    return c

def shuffleSwap(img):
    import random
    rindex=random.randint(0,6)
    gindex=random.randint(0,6)
    bindex=random.randint(0,6)
    for i in range(img.getHeight()):
        for j in range(img.getWidth()):
            p=img.getPixel(j,i)
            R,G,B=p.getRed(),p.getGreen(),p.getBlue()
            colors=[0]+[R,G,B]*2
            newRed=colors[rindex]
            newGreen=colors[gindex]
            newBlue=colors[bindex]
            newPixel=image.Pixel(newRed,newGreen,newBlue)
            img.setPixel(j,i,newPixel)
    c1=color_comp(rindex)
    c2=color_comp(gindex)
    c3=color_comp(bindex)
    components=(c1,c2,c3)
    return img,components
    
#16 Histogram
def drawHistogram(color,colorHis):
    colorHis.hideturtle()
    colorHis.begin_fill()
    for i in range(len(color)):
        colorHis.goto(i,color[i])
    colorHis.goto(255,0)
    colorHis.end_fill()

def histograms(img,choice):
    import turtle
    histo=turtle.Screen()
    histo.clearscreen()
    histo.tracer(2)
    t=[0]*256
    if choice=="1":
        red=t[:]
        for i in range(img.getHeight()):
            for j in range(img.getWidth()):
                p=img.getPixel(j,i)
                red[p.getRed()]+=1
        histo.setworldcoordinates(0,0,256,maxi(red)+20)
        redHis=turtle.Turtle()
        redHis.color("red")
        drawHistogram(red,redHis)
    elif choice=="2":
        green=t[:]
        for i in range(img.getHeight()):
            for j in range(img.getWidth()):
                p=img.getPixel(j,i)
                green[p.getGreen()]+=1
        histo.setworldcoordinates(0,0,256,maxi(green)+20)
        greenHis=turtle.Turtle()
        greenHis.color("green")
        drawHistogram(green,greenHis)
    elif choice=="3":
        blue=t[:]
        for i in range(img.getHeight()):
            for j in range(img.getWidth()):
                p=img.getPixel(j,i)
                blue[p.getBlue()]+=1
        histo.setworldcoordinates(0,0,256,maxi(blue)+20)
        blueHis=turtle.Turtle()
        blueHis.color("blue")
        drawHistogram(blue,blueHis)
    elif choice=="4":
        rgb=t[:]
        for i in range(img.getHeight()):
            for j in range(img.getWidth()):
                p=img.getPixel(j,i)
                avg=(p.getRed()+p.getGreen()+p.getBlue())//3
                rgb[avg]+=1
        histo.setworldcoordinates(0,0,256,maxi(rgb)+20)
        rgbHis=turtle.Turtle()
        rgbHis.color("grey")
        drawHistogram(rgb,rgbHis)
    else:
        red=t[:]
        green=t[:]
        blue=t[:]
        rgb=t[:]
        for i in range(img.getHeight()):
            for j in range(img.getWidth()):
                p=img.getPixel(j,i)
                avg=(p.getRed()+p.getGreen()+p.getBlue())//3
                rgb[avg]+=1
                red[p.getRed()]+=1
                green[p.getGreen()]+=1
                blue[p.getBlue()]+=1
        mr=maxi(red)
        mg=maxi(green)
        mb=maxi(blue)
        mx=maxi(rgb)
        maximum=[mr,mg,mb,mx]
        histo.setworldcoordinates(0,0,256,maxi(maximum)+20)
        redHis=turtle.Turtle()
        redHis.color("red")
        drawHistogram(red,redHis)
        greenHis=turtle.Turtle()
        greenHis.color("green")
        drawHistogram(green,greenHis)
        blueHis=turtle.Turtle()
        blueHis.color("blue")
        drawHistogram(blue,blueHis)
        rgbHis=turtle.Turtle()
        rgbHis.color("grey")
        drawHistogram(rgb,rgbHis)
    return histo

### Main function ###
def main(gif_file):
    img=image.Image(gif_file)
    fname=img.imFileName[:-4]
    win=image.ImageWin(fname+".gif",img.getWidth(),img.getHeight())
    img.draw(win)
    histo=False
    print("Python cImage Editor v0.4.0 beta\n by Alessandro De Marco\n")
    while True:
        choice=input("Select the filter you want to apply:\n 1) Crop\n 2) Rotate\n \
3) Flip\n 4) Enlarge X2\n 5) Brightness\n 6) Contrast\n 7) Saturation\n 8) Grayscale\n \
9) Sepia\n 10) Negative\n 11) Solarize\n 12) Posterize\n 13) Noise\n 14) HDR (Pseudo)\n \
15) Recolor\n 16) Show Histogram\n Press S to save the image\n Press Q to exit\n")
        if choice=="1":
            print("Select the area to crop:")
            img=crop(img,win)
            win._close()
            win=image.ImageWin(fname+".gif",img.getWidth(),img.getHeight())
            img.draw(win)
            print("\nImage cropped.\n")
        elif choice=="2":
            direction=input(" Rotate:\n L) Left\n R) Right\n")
            if direction in ["l","r"]:
                img=rotate(img,direction)
                win._close()
                win=image.ImageWin(fname+".gif",img.getWidth(),img.getHeight())
                img.draw(win)
                print("\nImage rotated.\n")
            else:
                print("Invalid input\n")
        elif choice=="3":
            axis=input(" Flip:\n 1) Horizontal\n 2) Vertical\n")
            if axis in ["1","2"]:
                img=flip(img,axis)
                img.draw(win)
                print("\nImage flipped.\n")
            else:
                print("Invalid input\n")
        elif choice=="4":
            print("Processing...")
            img=enlarge(img)
            win._close()
            win=image.ImageWin(fname+".gif",img.getWidth(),img.getHeight())
            img.draw(win)
            print("\nImage enlarged.\n")
        elif choice=="5":
            value=int(input("Set brightness between -255 and 255\n"))
            if value in range(-255,0) or value in range(1,256):
                print("Processing...\n")
                img=brightness(img,value)
                img.draw(win)
                if value>0:
                    print("Brightness increased by",value,"\n")
                else:
                    print("Brightness decreased by",abs(value),"\n")
            elif value==0:
                print("Image unchanged.\n")
            else:
                print("Invalid input\n")
        elif choice=="6":
            value=int(input("Set contrast between -255 and 255\n"))
            if value in range(-255,0) or value in range(1,256):
                print("Processing...\n")
                img=contrast(img,value)
                img.draw(win)
                if value>0:
                    print("Contrast increased by",value,"\n")
                else:
                    print("Contrast decreased by",abs(value),"\n")
            elif value==0:
                print("Image unchanged.\n")
            else:
                print("Invalid input\n")
        elif choice=="7":
            add=int(input("Increase/decrease saturation by: %"))
            if add in range(-100,0) or add in range(1,101):
                print("Processing...\n")
                img=RGBtoHSLtoRGB(img,add)
                img.draw(win)
                if add>0:
                    print("Saturation increased by",str(add)+"%\n")
                else:
                    print("Saturation decreased by",str(abs(add))+"%\n")
            elif add==0:
                print("\nImage unchanged.\n")
            else:
                print("\nInvalid input\n")
        elif choice=="8":
            print("Processing...")
            img=grayscale(img)
            img.draw(win)
            print("\nImage grayscaled.\n")
        elif choice=="9":
            print("Processing...")
            img=sepia(img)
            img.draw(win)
            print("\nSepia filter applied.\n")
        elif choice=="10":
            print("Processing...")
            img=invert(img)
            img.draw(win)
            print("\nImage inverted.\n")
        elif choice=="11":
            print("Processing...")
            img=solarize(img)
            img.draw(win)
            print("\nImage solarized.\n")
        elif choice=="12":
            print("Processing...")
            img=posterize(img)
            img.draw(win)
            print("\nImage posterized.\n")
        elif choice=="13":
            choice=input(" Choose type of noise:\n 1) Normal\n 2) Color noise\n")
            if choice=="1":
                print("Processing...")
                img=noise(img)
                img.draw(win)
                print("\nApplied.\n")
            elif choice=="2":
                print("Processing...")
                img=colorNoise(img)
                img.draw(win)
                print("\nApplied.\n")
            else:
                print("Invalid input\n")
        elif choice=="14":
            print("Processing...")
            img=RGBtoHSVtoRGB(img)
            img.draw(win)
            print("\nApplied.\n")
        elif choice=="15":
            choice=input(" Turn the image:\n 1) Red\n 2) Green\n 3) Blue\n 4) Cyan\n \
5) Yellow\n 6) Magenta\n 7) Blue <> Green\n 8) Blue <> Red\n 9) Green <> Red\n 10) Green \
<> Blue <> Red\n 11) Blue <> Red <> Green\n 12) Random\n")
            if choice in ["1","2","3","4","5","6","7","8","9","10","11"]:
                print("Processing...")
                img=recolor(img,choice)
                img.draw(win)
                print("\nApplied.\n")
            elif choice=="12":
                print("Processing...")
                img,comp=shuffleSwap(img)
                img.draw(win)
                print("\nPixel components are now",str(comp)+".\n")
            else:
                print("Invalid input\n")
        elif choice=="16":
            choice=input(" 1) Red\n 2) Green\n 3) Blue\n 4) RGB\n 5) All\n")
            if choice in ["1","2","3","4","5"]:
                histo=histograms(img,choice)
            else:
                print("Invalid input\n")
        elif choice=="s":
            img.saveTk(fname+"-edited.gif")
            print("Image saved.\n")
        elif choice=="q":
            if histo:
                histo.bye()
            win._close()
            return False
        else:
            print("Invalid input\n")
        print("------------------------------------")

# main call
import cImage as image
main("pizzo.gif")
