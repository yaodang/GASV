*---------------------------------------------------------
*install(linux):
*       gfortran -shared -fPIC MAT_INV.F -o MAT_INV.so -llapack -lblas
*install(windows):
*       gfortran -shared -fPIC MAT_INV.F -o MAT_INV.so -llapack -lblas
*--------------------------------------------------------      

      SUBROUTINE MAT_INV(A, A_INV, N, INFO)
      IMPLICIT NONE
      
      INTEGER, INTENT(IN) :: N
      INTEGER, INTENT(OUT) :: INFO
      REAL*8, INTENT(IN), DIMENSION(N,N) :: A
      REAL*8, INTENT(OUT), DIMENSION(N,N) :: A_INV
      
      INTEGER, ALLOCATABLE :: IPIV(:)
      REAL*8, ALLOCATABLE :: WORK(:)
      INTEGER :: LWORK
      
      ALLOCATE(IPIV(N))
      
      A_INV = A
      
      CALL DGETRF(N, N, A_INV, N, IPIV, INFO)
      
      IF (INFO /= 0) THEN
          DEALLOCATE(IPIV)
          RETURN
      END IF
      
      LWORK = -1
      ALLOCATE(WORK(1))
      CALL DGETRI(N, A_INV, N, IPIV, WORK, LWORK, INFO)
      LWORK = INT(WORK(1))
      DEALLOCATE(WORK)
      
      ALLOCATE(WORK(LWORK))
      
      CALL DGETRI(N, A_INV, N, IPIV, WORK, LWORK, INFO)
      
      DEALLOCATE(IPIV, WORK)
      
      END SUBROUTINE MAT_INV
