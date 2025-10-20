import numpy as np
import timeit
from matrix_fort import inverse_matrix

def test_performance():
    # 测试不同矩阵大小
    sizes = [100, 500, 1000, 2000]
    num_runs = 5
    
    for n in sizes:
        # 生成随机矩阵
        A = np.random.rand(n, n)
        # 确保矩阵可逆
        A = A @ A.T + 0.01 * np.eye(n)
        
        # 测试NumPy
        numpy_time = timeit.timeit(lambda: np.linalg.inv(A), number=num_runs)
        numpy_avg = numpy_time / num_runs
        
        # 测试Fortran
        def fortran_inv():
            A_inv = np.zeros_like(A)
            info = np.zeros(1, dtype=np.int32)
            inverse_matrix(A, n, A_inv, info)
            return A_inv
        
        fortran_time = timeit.timeit(fortran_inv, number=num_runs)
        fortran_avg = fortran_time / num_runs
        
        # 计算速度比
        speedup = numpy_avg / fortran_avg
        
        print(f"矩阵大小: {n}x{n}")
        print(f"NumPy平均时间: {numpy_avg:.6f}秒")
        print(f"Fortran平均时间: {fortran_avg:.6f}秒")
        print(f"速度比: {speedup:.2f}x")
        print("-" * 50)

if __name__ == "__main__":
    test_performance()
