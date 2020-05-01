PROGRAM MALUSv001
!   Make sure that data does NOT have leap days.
!   Check if temperatures are in Fahrenheit or Celsius.
!   Check if temperatures are integers or reals.
!   Check if precip is in millimeters or inches.
!   Check if there is a header.
!
!    Implicit None
    REAL A,TAVG,CDH,TMAX,TMIN,CDHTOT
! CHLTOT, PHI
    REAL STAGE,YLD,rprecip,DAM,FDIAMT,FDIAMS
!rmax,rmin,rsr
    INTEGER YR,MO,DAY,CD,nyr
    REAL imax,imin
!sr, iflag,precip
    integer fgreen(200),bloom(200),bflag,pdays,INJDAYS
    integer stage3, stage4, stage5, stage6, stage7, stage9, counter
    integer wstage3, wstage4, wstage5, wstage6, wstage7, wstage9

    character*300 input, output1, output2, header

    input="./42.96_-85.67_1981-2018.txt"
    output1="./42.96_-85.67_daily.txt"
    output2="./42.96_-85.67_yearly.txt"

    OPEN(1,FILE=input,STATUS='OLD')
    OPEN(2,FILE=output1,STATUS='UNKNOWN')
    OPEN(3,FILE=output2,STATUS='UNKNOWN')
!
 !       write(3,*) "year  stage2  stage3  stage4  stage5  stage6 &
 !       & stage7  stage8  stage9  yield index  poor pdays"

!   read the header
    read(1,*) header

!	READ THE DATA
    counter=0
    DO 100 J=1,1000000
       CDHTOT=0.0
        sflag=0
        bflag=0
        YLD=1.0
        DAM=0.0
        STAGE=0.0
        RGDD=0.0
        FDIAMT=0.0
        FDIAMS=0.0
        pdays=0
        GDD = 0.0
        INJDAYS=0

        stage3=0
        stage4=0
        stage5=0
        stage6=0
        stage7=0
        stage9=0
        counter=counter+1

!	WEATHER DATA INPUT (year, month, day, Tmax (F),Tmin (F), precip (inches))

        DO 200 K=1,365
            READ(1,*,end=500) yr, mo, day, imax, imin, rprecip

!   Check if there are any missing data (-9999)
            if (imin<-99 .or. imax<-99 .or. rprecip<-99) then
                print*, "missing data!!!", yr,mo,day,imax,imin,rprecip
            endif

!   Convert Fahrenheit to Celsius
!            TMAX=(5./9.)*(imax-32.)
!            TMAX = float (imax)
!            TMIN = float (imin)
            TMAX = imax
            TMIN = imin
            !            TMIN=(5./9.)*(imin-32.)

            if(tmax.le.tmin) tmax=tmin+0.05

!   Calculate calendar day (1-365)
            IF(MO.EQ.1) CD=MO*30.6-30.3+DAY
            IF(MO.EQ.2) CD=MO*30.6-29.3+DAY
            IF(MO.GE.3) CD=MO*30.6-32.3+DAY
!
!	INITIALIZE AVG TEMP, AMPLITUDE, AND BASE TEMP(here set at 42F)
!
!	if(yr.eq.1990.and.cd.eq.1) goto 201
            if(mo.lt.3) goto 201
            A=(TMAX-TMIN)/2.
            TAVG=(TMAX+TMIN)/2.
            TBASE=42.0
            CDH=0.0
            CHLD=0.0
!
!    THIS ROUTINE NEEDS TO BE FED MAX AND MIN TEMPERATURES
!    (TMAX AND TMIN) AND A BASE TEMPERATURE (TBASE).  THE OUTPUT
!    IS THE VARIABLE NAME 'GDD'.
!
!  TEST DATA TO DETERMINE WHICH TEST TO USE
            IF (TMAX.LE.TBASE) GOTO 570
            TAVG=(TMAX+TMIN)/2
            IF (TMIN.GE.TBASE) GOTO 565
!  CALCULATION ROUTINE - MAX GREATER THAN BASE, BUT MIN LESS THAN BASE
            W=(TMAX-TMIN)/2
!      print*, w
            Y=(TBASE-TAVG)/W
!	print*, y
            if(y.eq.-1.0) y=-0.9999
            if(y.eq.1.0) y=0.9999
            A=ATAN(Y/SQRT(-Y*Y+1))
!	print*, a
            BE1=((W*COS(A)-(TBASE-TAVG)*(3.1415927/2-A))/3.1415927)
!	print*, be1
!      print*, tmax,tmin,w,y,a,be1
            GOTO 567
!  CALCULATION ROUTINE FOR MIN GREATER THAN BASE
565         BE1=TAVG-TBASE
567         GDD=BE1
            GOTO 572
570         GDD=0.0
572         cdhtot=cdhtot+gdd

!	IF(SFLAG.EQ.1) GOTO 199
!
!   THIS PHENOLOGY ROUTINE IS FOR A SGDD42 STARTING 1 MAR (based on Schwallier peach ridge data with Macintosh)
!
            IF (CDHTOT.LT.90.) then
                STAGE=1
            Else IF(CDHTOT.GE.90.AND.CDHTOT.LT.127.) THEN
                STAGE=2
                if(sflag.eq.1) goto 199
                SFLAG=1
                fgreen(J)=cd
            Else if(CDHTOT.GE.127.AND.CDHTOT.LT.205.) THEN
                STAGE=3
                stage3=stage3+1
                if (stage3 == 1) then
                    wstage3 = cd
                endif
            Else if(CDHTOT.GE.205.AND.CDHTOT.LT.242.) THEN
                STAGE=4
               stage4=stage4+1
                if (stage4 == 1) then
                    wstage4 = cd
                endif
            Else if(CDHTOT.GE.242.AND.CDHTOT.LT.284.) THEN
                STAGE=5
                stage5=stage5+1
                if (stage5 == 1) then
                    wstage5 = cd
                endif
            Else IF(CDHTOT.GE.284.AND.CDHTOT.LT.367.) THEN
                STAGE=6
               stage6=stage6+1
                if (stage6 == 1) then
                    wstage6 = cd
                endif
            Else IF(CDHTOT.GE.367.AND.CDHTOT.LT.422.) THEN
                STAGE=7
               stage7=stage7+1
                if (stage7 == 1) then
                    wstage7 = cd
                endif
            Else IF(CDHTOT.GE.422.AND.CDHTOT.LT.511.) THEN
                STAGE=8
                if(bflag.eq.1) goto 199
                bflag=1
                bloom(j)=cd
!	    if(rprecip.gt.0.0) pdays=pdays+1
            Else IF(CDHTOT.GE.511.) THEN
                STAGE=9
                stage9=stage9+1
                if (stage9 == 1) then
                    wstage9 = cd
                endif
            ENDIF
!		REPRODUCTIVE STAGE PHENOLOGY FOR TART CHERRY
!
!	THIS ROUTINE IS INITITALIZED AT PETAL FALL (VSTAGE 9)
!	   THE REGRESSIONS FOR TERMINAL AND SHOOT FRUIT WERE
!	   BASED ON UNPUBLISHED PHENO DATA OF J FLORE.
!
199         if(stage.eq.8.and.(tavg.lt.50.0.or.rprecip.gt.0.0)) pdays=pdays+1
!	if(stage.eq.8.and.rprecip.gt.0.0) pdays=pdays+1
            IF(STAGE.GE.2.AND.SFLAG.EQ.1) THEN
                RGDD=RGDD+GDD
                IF(RGDD.GT.1200) RGDD=1200.
                FDIAMT=100/(1+(EXP(3.2418-(0.0218*RGDD)+(0.0000452*RGDD**2)- &
                 (3.446E-08*RGDD**3))))
!	FDIAMS=-16.75936+(0.14866*RGDD)-(0.00031699*RGDD**2)+
!     !(3.208445E-07*RGDD**3)-(1.1644E-10*RGDD**4)
                IF(FDIAMT.LT.10.) FDIAMT=10.0
                IF(FDIAMS.LT.2.) FDIAMS=2.0
            endif
            if(fdiamt.gt.100.) fdiamt=100.
            IF(rgdd.GT.1200.0) THEN
                SFLAG=0
            ENDIF
!
!		COLD INJURY ROUTINE
!       TEMP THRESHOLDS BASED ON WSU EB1240 
!       https://www.canr.msu.edu/uploads/396/36740/PictureTableofFruitFreezeDamageThresholds.pdf
!
201         if(cd.gt.213) goto 203

!	DAMAGE DURING DORMANCY
            iF(TMIN .LT. -25.0 .AND. STAGE .EQ. 0) THEN
                YLD=YLD*0.5
                INJDAYS=INJDAYS+1
!	STAGE 2 DAMAGE
            Else IF(STAGE.EQ.2.AND.TMIN.LE.2.0) THEN
                DAM=0.9
            Else IF(STAGE.EQ.2.AND.TMIN.gt.2.0.AND.TMIN.LE.15.) THEN
                DAM=(-0.06154*TMIN+1.023077)
                if(dam.lt.0.0) dam=0.0
                YLD=YLD-(YLD*DAM)
                INJDAYS=INJDAYS+1
                if(yld.lt.0.0) yld=0.01
!	 STAGE 3 DAMAGE
            Else IF(STAGE.EQ.3.AND.TMIN.LE.10.0) THEN
                DAM=0.9
            Else IF(STAGE.EQ.3.AND.TMIN.gt.10.0.AND.TMIN.LE.18.) THEN
                DAM=(-0.1*TMIN+1.9)
                if(dam.lt.0.0) dam=0.0
                YLD=YLD-(YLD*DAM)
                INJDAYS=INJDAYS+1
                if(yld.lt.0.0) yld=0.01
!	  STAGE 4 DAMAGE
            Else IF(STAGE.EQ.4.AND.TMIN.LE.15.0) THEN
                DAM=0.9
            Else IF(STAGE.EQ.4.AND.TMIN.gt.15.0.AND.TMIN.LE.23.) THEN
                DAM=(-0.1*TMIN+2.4)
                if(dam.lt.0.0) dam=0.0
                YLD=YLD-(YLD*DAM)
                INJDAYS=INJDAYS+1
                if(yld.lt.0.0) yld=0.01
!	    STAGE 5 DAMAGE
            Else IF(STAGE.EQ.5.AND.TMIN.LE.21.0) THEN
                DAM=0.9
            Else IF(STAGE.EQ.5.AND.TMIN.gt.21.0.AND.TMIN.LE.27.) THEN
                DAM=(-0.13333*TMIN+3.7)
                if(dam.lt.0.0) dam=0.0
                YLD=YLD-(YLD*DAM)
                INJDAYS=INJDAYS+1
                if(yld.lt.0.0) yld=0.01
!	     STAGE 6 DAMAGE
            Else IF(STAGE.EQ.6.AND.TMIN.LE.24.0) THEN
                DAM=0.9
            Else IF(STAGE.EQ.6.AND.TMIN.gt.24.0.AND.TMIN.LE.28.) THEN
                DAM=(-0.2*TMIN+5.7)
                if(dam.lt.0.0) dam=0.0
                YLD=YLD-(YLD*DAM)
                INJDAYS=INJDAYS+1
                if(yld.lt.0.0) yld=0.01
!	      STAGE 7 DAMAGE
            Else IF(STAGE.EQ.7.AND.TMIN.LE.25.0) THEN
                DAM=0.9
            Else IF(STAGE.EQ.7.AND.TMIN.gt.25.0.AND.TMIN.LE.28.) THEN
                DAM=(-0.2667*TMIN+7.566667)
                if(dam.lt.0.0) dam=0.0
                YLD=YLD-(YLD*DAM)
                INJDAYS=INJDAYS+1
                if(yld.lt.0.0) yld=0.01
!	       STAGE 8 DAMAGE
            Else IF(STAGE.EQ.8.AND.TMIN.LE.25.0) THEN
                DAM=0.9
            Else IF(STAGE.EQ.8.AND.TMIN.gt.25.0.AND.TMIN.LE.28.) THEN
                DAM=(-0.2667*TMIN+7.566667)
                if(dam.lt.0.0) dam=0.0
                INJDAYS=INJDAYS+1
                YLD=YLD-(YLD*DAM)
                if(yld.lt.0.0) yld=0.01
!	       STAGE 9 DAMAGE
            Else IF(STAGE.GE.9.AND.TMIN.LE.25.0) THEN
                DAM=0.9
            Else IF(STAGE.GE.9.AND.TMIN.gt.25.0.AND.TMIN.LE.28.) THEN
                DAM=(-0.2667*TMIN+7.566667)
                if(dam.lt.0.0) dam=0.0
                YLD=YLD-(YLD*DAM)
                INJDAYS=INJDAYS+1
                if(yld.lt.0.0) yld=0.01
            ENDIF
203        WRITE(2,10)YR,cd,TMAX,TMIN,gdd,CDHTOT,STAGE,DAM,YLD,INJDAYS
10          FORMAT(2I6,5F10.1,2F10.2,I6)
!10          FORMAT(F4.0,F3.0,5F10.1,2F10.2,I6)
            DAM=0.0
200     continue

        RGG=0.0
        SFLAG=0
        bflag=0
!        print*, yr, fgreen(j), bloom(j), yld, INJDAYS,pdays
        write(3,11) yr, fgreen(j), bloom(j), yld, INJDAYS,pdays

 !       write(3,19) yr, fgreen(j),wstage3,wstage4,wstage5,wstage6,wstage7, bloom(j),wstage9, yld, pdays

!19      format(9i8,f8.2,i6)
11      format(i6,2i10,f8.2,2i6)
!11      format(F6.0,2i10,f8.2,2i6)
        PDAYS=0
        INJDAYS=0
100 continue
    stop
500 print*, yr, fgreen(j), bloom(j), yld, pdays
!    write(3,11) yr, fgreen(j), bloom(j), yld, pdays

End program

