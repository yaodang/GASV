subroutine inverse_matrix(A, n, A_inv, info)
    implicit none
    integer, intent(in) :: n
    real*8, intent(in) :: A(n,n)
    real*8, intent(out) :: A_inv(n,n)
    integer, intent(out) :: info
    
    real*8, allocatable :: work(:)
    integer, allocatable :: ipiv(:)
    integer :: lwork, i
    
    ! 复制输入矩阵到输出矩阵，避免修改原矩阵
    A_inv = A
    
    ! 获取最优工作空间大小
    lwork = -1
    allocate(work(1))
    call dgetri(n, A_inv, n, ipiv, work, lwork, info)
    lwork = int(work(1))
    deallocate(work)
    
    ! 分配工作空间和 pivot 数组
    allocate(work(lwork))
    allocate(ipiv(n))
    
    ! 计算LU分解
    call dgetrf(n, n, A_inv, n, ipiv, info)
    if (info /= 0) then
        deallocate(work, ipiv)
        return
    end if
    
    ! 计算逆矩阵
    call dgetri(n, A_inv, n, ipiv, work, lwork, info)
    
    deallocate(work, ipiv)
end subroutine inverse_matrix
