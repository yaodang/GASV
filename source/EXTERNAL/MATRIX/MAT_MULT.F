*---------------------------------------------------------------------------
*install:
*        gfortran -shared -fPIC MAT_MULT.F -o MAT_MULT.so -lopenblas
*---------------------------------------------------------------------------
      SUBROUTINE MAT_MULT(A, B, C, M, N, K)
      IMPLICIT NONE
      
      ! 输入/输出参数
      INTEGER, INTENT(IN) :: M, N, K
      REAL*8, INTENT(IN), DIMENSION(M,K) :: A
      REAL*8, INTENT(IN), DIMENSION(K,N) :: B
      REAL*8, INTENT(OUT), DIMENSION(M,N) :: C
      
      ! 局部变量
      INTEGER :: LDA, LDB, LDC
      REAL*8 :: ALPHA, BETA
      CHARACTER :: TA, TB
      
      TA = 'N'  ! N or T for A transposition
      TB = 'N'  ! N or T for  B transposition
      LDA = M       ! A leading dimension
      LDB = K       ! B leading dimension
      LDC = M       ! C leading dimension
      ALPHA = 1.0D0 
      BETA = 0.0D0  ! 0: initialize C to  0
      
      
      ! call DGEMM function
      CALL DGEMM(TA, TB, M, N, K, ALPHA, A, LDA, B, LDB, BETA, C, LDC)
      !CALL DGEMM('N', 'N', M, N, K, ALPHA, A, LDA, B, LDB, BETA, C, LDC)
    
      END SUBROUTINE MAT_MULT
