SUBROUTINE CERASUS_v64(input, output1, output2)
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
!    REAL imax,imin
!sr, iflag,precip
    integer sidegreen(200),bloom(200),bflag,pdays

    character*300 input, output1, output2, header


    OPEN(1,FILE=input,STATUS='OLD')
    OPEN(2,FILE=output1,STATUS='UNKNOWN')
    OPEN(3,FILE=output2,STATUS='UNKNOWN')

!   read the header
    read(1,*) header

!	READ THE DATA
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

!	WEATHER DATA INPUT (year, month, day, Tmax (F),Tmin (F), precip (inches))

        DO 200 K=1,365
            READ(1,*,end=500) yr, mo, day, tmax, tmin, rprecip

!   Check if there are any missing data (-9999)
            if (tmin<-99 .or. tmax<-99 .or. rprecip<-99) then
                print*, "missing data!!!", yr,mo,day,tmax,tmin,rprecip
            endif


            TMAX=(5./9.)*(TMAX-32.)
            TMIN=(5./9.)*(TMIN-32.)
            
            if(tmax.le.tmin) tmax=tmin+0.05

!   Calculate calendar day (1-365)
            IF(MO.EQ.1) CD=MO*30.6-30.3+DAY
            IF(MO.EQ.2) CD=MO*30.6-29.3+DAY
            IF(MO.GE.3) CD=MO*30.6-32.3+DAY
!
!	INITIALIZE AVG TEMP, AMPLITUDE, AND BASE TEMP(here set at 4C)
!
!	if(yr.eq.1990.and.cd.eq.1) goto 201
            if(yr.eq.1981.and.cd.eq.1) goto 201
            A=(TMAX-TMIN)/2.
			TAVG=(TMAX+TMIN)/2.
			TBASE=4.0
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
            A=ATAN(Y/SQRT(-Y*Y+1))
            BE1=((W*COS(A)-(TBASE-TAVG)*(3.1415927/2-A))/3.1415927)
            GOTO 567
!  CALCULATION ROUTINE FOR MIN GREATER THAN BASE
565         BE1=TAVG-TBASE
567         GDD=BE1
            GOTO 572
570         GDD=0.0
!
!  BEGIN SEASONAL GDD ACCUMS 1 MAR
!
572        	IF(CD.LE.60) GOTO 574
			cdhtot=cdhtot+gdd
!	IF(SFLAG.EQ.1) GOTO 199
!
!   THIS PHENOLOGY ROUTINE IS FOR A SGDD4 STARTING 1 MAR (based on Zavalloni et al (2009) tart cherry phenology routine)
!
574         IF (CDHTOT.LT.120.) THEN
                STAGE=0
                GOTO 201
            Else IF(CDHTOT.GE.120.AND.CDHTOT.LT.154.) THEN
                STAGE=2
                if(sflag.eq.1) goto 199
                SFLAG=1
                sidegreen(J)=cd
                GOTO 199
            Else if(CDHTOT.GE.154.AND.CDHTOT.LT.174.) THEN
                STAGE=3
                GOTO 199
            Else if(CDHTOT.GE.174.AND.CDHTOT.LT.190.) THEN
                STAGE=4
                GOTO 199
            Else if(CDHTOT.GE.190.AND.CDHTOT.LT.208.) THEN
                STAGE=5
                GOTO 199
            Else IF(CDHTOT.GE.208.AND.CDHTOT.LT.228.) THEN
                STAGE=6
                GOTO 199
            Else IF(CDHTOT.GE.228.AND.CDHTOT.LT.253.) THEN
                STAGE=7
                GOTO 199
            Else IF(CDHTOT.GE.253.AND.CDHTOT.LT.311.) THEN
                STAGE=8
                if(rprecip.gt.0.0) pdays=pdays+1
                if(bflag.eq.1) goto 199
                bflag=1
                bloom(j)=cd
                GOTO 199
            Else IF(CDHTOT.GE.321.) THEN
                STAGE=9
                GOTO 199
            ENDIF
!		REPRODUCTIVE STAGE PHENOLOGY FOR TART CHERRY
!
!	THIS ROUTINE IS INITITALIZED AT PETAL FALL (VSTAGE 9)
!	   THE REGRESSIONS FOR TERMINAL AND SHOOT FRUIT WERE
!	   BASED ON UNPUBLISHED PHENO DATA OF J FLORE.
!
199          IF(STAGE.GE.2.AND.SFLAG.EQ.1) THEN
                RGDD=RGDD+GDD
                IF(RGDD.GT.1200) RGDD=1200.
                FDIAMT=100/(1+(EXP(3.2418-(0.0218*RGDD)+(0.0000452*RGDD**2))))
!     (3.446E-08*RGDD**3))))
                IF(FDIAMT.LT.10.) FDIAMT=10.0
                IF(FDIAMS.LT.2.) FDIAMS=2.0
            ENDIF
            if(fdiamt.gt.100.) fdiamt=100.
            IF(rgdd.GT.1200.0) THEN
                SFLAG=0
            ENDIF
!
!		COLD INJURY ROUTINE
!       TEMP THRESHOLDS BASED ON WSU EB1240 
!       https://www.canr.msu.edu/uploads/396/36740/PictureTableofFruitFreezeDamageThresholds.pdf
!
201         if(CD.gt.213) goto 203
! DAMAGE DURING DORMANCY
			iF(TMIN.LT.-34.4.AND.STAGE.EQ.0) THEN
				DAM=Yld*0.5
				if(dam.lt.0.0) dam=0.0
				YLD=YLD-DAM
				if(yld.lt.0.0) yld=0.01
				GOTO 203
			ENDIF
!			IF(TMIN.LT.-31.6.AND.STAGE.EQ.0) THEN
!				DAM=Yld*0.5
!				if(dam.lt.0.0) dam=0.0
!				YLD=YLD-DAM
!				if(yld.lt.0.0) yld=0.01
!				GOTO 203
!			ENDIF
! STAGE 2 DAMAGE
			IF(STAGE.EQ.2.AND.TMIN.LE.-4.4) THEN
				DAM=(-2.83*TMIN+10.43)/100.
				if(dam.lt.0.0) dam=0.0
				YLD=YLD-DAM
				if(yld.lt.0.0) yld=0.01
				GOTO 203
			ENDIF
!	 STAGE 3 DAMAGE
			IF(STAGE.EQ.3.AND.TMIN.LE.-3.3) THEN
				DAM=(-5.16*TMIN+1.59)/100.
				if(dam.lt.0.0) dam=0.0 
				YLD=YLD-DAM
				if(yld.lt.0.0) yld=0.01 
				GOTO 203
			ENDIF
!	  STAGE 4 DAMAGE
			IF(STAGE.EQ.4.AND.TMIN.LE.-3.3) THEN
				DAM=(-5.19*TMIN-6.41)/100.
				if(dam.lt.0.0) dam=0.0 
				YLD=YLD-DAM
				if(yld.lt.0.0) yld=0.01 
				GOTO 203
			ENDIF
!	    STAGE 5 DAMAGE
			IF(STAGE.EQ.5.AND.TMIN.LE.-2.2) THEN			   
				DAM=(-4.7936*TMIN-0.2189)/100.
				if(dam.lt.0.0) dam=0.0 
				YLD=YLD-DAM
				if(yld.lt.0.0) yld=0.01 
				GOTO 203
			ENDIF
!	     STAGE 6 DAMAGE
			IF(STAGE.EQ.6.AND.TMIN.LE.-2.2) THEN			   
				DAM=(-4.7936*TMIN-0.2189)/100.
				if(dam.lt.0.0) dam=0.0
				YLD=YLD-DAM
				if(yld.lt.0.0) yld=0.01 
				GOTO 203
			ENDIF 
!	      STAGE 7 DAMAGE
			IF(STAGE.EQ.7.AND.TMIN.LE.-2.2) THEN			   
				DAM=(-4.7936*TMIN-0.2189)/100.
				if(dam.lt.0.0) dam=0.0 
				YLD=YLD-DAM
				if(yld.lt.0.0) yld=0.01 
				GOTO 203
			ENDIF	     		     	     		     	     		     	     
!	       STAGE 8 DAMAGE
			IF(STAGE.gE.8.AND.TMIN.LE.-2.2) THEN			   
				if(cd.gt.244) goto 203
				DAM=(-4.7936*TMIN-0.2189)/100.
				if(dam.lt.0.0) dam=0.0 
				YLD=YLD-DAM
				if(yld.lt.0.0) yld=0.01 
				GOTO 203
			ENDIF
203        WRITE(2,10)YR,cd,TMAX,TMIN,rprecip,gdd,CDHTOT,STAGE,rgdd,FDIAMT,FDIAMS,DAM,YLD
10          FORMAT(2I6,11F10.2)
            DAM=0.0
200     continue

        RGG=0.0
        SFLAG=0
        bflag=0
        write(3,11) yr,sidegreen(j),bloom(j),pdays,yld


11      format(i6,2i10,i6,f8.2)
        PDAYS=0
100 continue
    stop
500 print*, yr, sidegreen(j), bloom(j), yld, pdays
End subroutine CERASUS_v64

PROGRAM MAIN
    character*300 :: input,output1,output2
    character*300 inputfile, outputfile1, outputfile2
    
    OPEN(11,FILE='input_list.txt',STATUS='OLD')
    OPEN(12,FILE='output_daily_list.txt',STATUS='OLD')
    OPEN(13,FILE='output_yearly_list.txt',STATUS='OLD')
!    OPEN(11,FILE='input_list_test.txt',STATUS='OLD')
!    OPEN(12,FILE='output_daily_list_test.txt',STATUS='OLD')
!    OPEN(13,FILE='output_yearly_list_test.txt',STATUS='OLD')
    do i=1,1000000000
        read(11, *)inputfile
        input = "./input/GDD_input/"//inputfile
        read(12, *)outputfile1
        output1 = "./output_Cherry/daily/"//outputfile1
!        output1 = "zz_"//outputfile1
        read(13, *)outputfile2
        output2 = "./output_Cherry/yearly/"//outputfile2
!        output2 = "zz_"//outputfile2
        call CERASUS_v64(input, output1, output2)
    end do
    CLOSE(11, STATUS='KEEP') 
    CLOSE(12, STATUS='KEEP') 
    CLOSE(13, STATUS='KEEP') 
end program


