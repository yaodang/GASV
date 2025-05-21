      SUBROUTINE OTC (DT,TAMP,TPH,IRNT,SAMP,DZO,DSO,DWO)
*-----------------------------------------------------------------------

      IMPLICIT NONE
      INTEGER I,IDAY,IDT,IMONTH,IRNT,IRHI,IRLI,IT,LUO,NB,NL,NP,NT,NTIN,
     .        KK,NTOUT,MDAY
      INTEGER DT
*+---------------------------------------------------------------------
*
*  Parameters below set the buffer size for computing the tides
*  recursively (nl), the number of harmonics used in the prediction
*  (nt; this must also be set in the subroutine admint) and the number
*  of harmonics read in (ntin)
*
*----------------------------------------------------------------------
      PARAMETER (NL=1)
      PARAMETER (NT=342)
      PARAMETER (NTIN=11)

      CHARACTER*40 DUMM
      REAL, intent(out) :: DWO,DZO,DSO
      REAL AMP,AS,AW,AZ,DZ,DW,DS,HCS,HCW,HCZ,PHASE,TAMP,TPH,WF,SAMP
      DOUBLE PRECISION F,PZ,PS,PW,SCR
      DOUBLE PRECISION DR,PI

      DIMENSION TAMP(3,NTIN),TPH(3,NTIN)
      DIMENSION IDT(6,NTIN),AMP(NTIN),PHASE(NTIN)
      DIMENSION AZ(NT),PZ(NT),HCZ(2*NT)
      DIMENSION AS(NT),PS(NT),HCS(2*NT)
      DIMENSION AW(NT),PW(NT),HCW(2*NT)
      DIMENSION DZ(NL),DS(NL),DW(NL)
      DIMENSION F(NT),SCR(3*NT),WF(NT)
      DIMENSION DT(5)
      COMMON/DATE/IT(5)
      DATA DR/0.01745329252D0/,IRLI/1/
      PARAMETER ( PI = 3.1415926535897932384626433D0 ) 
      DATA LUO/6/

*  Cartwright-Tayler numbers of tides used in Scherneck lists:
*      M2, S2, N2, K2, K1, O1, P1, Q1, Mf, Mm, Ssa

      DATA IDT/
     .  2, 0, 0, 0, 0, 0,   2, 2,-2, 0, 0, 0,   2,-1, 0, 1, 0, 0,
     .  2, 2, 0, 0, 0, 0,   1, 1, 0, 0, 0, 0,   1,-1, 0, 0, 0, 0,
     .  1, 1,-2, 0, 0, 0,   1,-2, 0, 1, 0, 0,   0, 2, 0, 0, 0, 0,
     .  0, 1, 0,-1, 0, 0,   0, 0, 2, 0, 0, 0/

      DO I=1,5
        IT(I) = DT(I)
!        WRITE(LUO,124) (DT(I))
! 124    FORMAT(1I14)      
      ENDDO
*+---------------------------------------------------------------------
* Change sign for phase, to be negative for lags
*----------------------------------------------------------------------
      DO I=1,3
        DO KK=1,NTIN
          TPH(I,KK)=-TPH(I,KK)
        ENDDO
      ENDDO
*+---------------------------------------------------------------------
*
*  Find amplitudes and phases for all constituents, for each of the
*  three displacements. Note that the same frequencies are returned 
*  each time.
*
*  BLQ format order is vertical, horizontal EW, horizontal NS
*
*----------------------------------------------------------------------
      DO I=1,NTIN
        AMP(I)=TAMP(1,I)
!        WRITE(LUO,122) (TAMP(1,I))
! 122    FORMAT(1F14.6)
        PHASE(I)=TPH(1,I)
      ENDDO
      CALL ADMINT(AMP,IDT,PHASE,AZ,F,PZ,NTIN,NTOUT)
      DO I=1,NTIN
        AMP(I)=TAMP(2,I)
        PHASE(I)=TPH(2,I)
      ENDDO
      CALL ADMINT(AMP,IDT,PHASE,AW,F,PW,NTIN,NTOUT)
      DO I=1,NTIN
        AMP(I)=TAMP(3,I)
        PHASE(I)=TPH(3,I)
      ENDDO
      CALL ADMINT(AMP,IDT,PHASE,AS,F,PS,NTIN,NTOUT)

*  set up for recursion, by normalizing frequencies, and converting
*  phases to radians

      DO I=1,NTOUT
        PZ(I) = DR*PZ(I)
        PS(I) = DR*PS(I)
        PW(I) = DR*PW(I)
        F(I) = SAMP*PI*F(I)/43200.D0
        WF(I) = F(I)
      ENDDO

*+---------------------------------------------------------------------
*
*  Loop over times, nl output points at a time. At the start of each
*  such block, convert from amp and phase to sin and cos (hc array) at
*  the start of the block. The computation of values within each
*  block is done recursively, since the times are equi-spaced.
*
*----------------------------------------------------------------------

 11   IRHI = MIN(IRLI+NL-1,IRNT)
      NP = IRHI - IRLI + 1
!      WRITE(LUO,123) IRHI,NP,IRNT
! 123  FORMAT(1I14,1I14,1I14)

* Set up harmonic coefficients, compute tide, and write out
      DO I=1,NT
        HCZ(2*I-1) = AZ(I)*DCOS(PZ(I))
        HCZ(2*I)  = -AZ(I)*DSIN(PZ(I))
        HCS(2*I-1) = AS(I)*DCOS(PS(I))
        HCS(2*I)  = -AS(I)*DSIN(PS(I))
        HCW(2*I-1) = AW(I)*DCOS(PW(I))
        HCW(2*I)  = -AW(I)*DSIN(PW(I))
      ENDDO
      CALL RECURS(DZ,NP,HCZ,NTOUT,WF,SCR)
      CALL RECURS(DS,NP,HCS,NTOUT,WF,SCR)
      CALL RECURS(DW,NP,HCW,NTOUT,WF,SCR)
      DZO = DZ(1)
      DSO = DS(1)
      DWO = DW(1)
!      WRITE(LUO,120) (DZ(I),DS(I),DW(I),I=1,NP)
! 120  FORMAT(3F14.6)     
!      WRITE(LUO,120) DZO,DSO,DWO
! 120  FORMAT(1F14.6,1F14.6,1F14.6)     
!      IF(IRHI.EQ.IRNT) STOP
!      IRLI = IRHI + 1

*  Reset phases to the start of the new section
!      DO I=1,NT
!        PZ(I) = DMOD(PZ(I) + NP*F(I),2.D0*PI)
!        PS(I) = DMOD(PS(I) + NP*F(I),2.D0*PI)
!        PW(I) = DMOD(PW(I) + NP*F(I),2.D0*PI)
!      ENDDO
      !GO TO 11

*  Finished.

*+----------------------------------------------------------------------
      END
