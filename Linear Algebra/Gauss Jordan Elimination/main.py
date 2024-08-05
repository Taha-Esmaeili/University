import numpy as np

# تعریف تابع اصلی
def Gaussian_Jordan_Elimination(A, b):
    # کنترل ابعاد ماتریس‌ها
    if A.shape[0] != b.shape[0]:
        return print('تعداد سطرهای ماتریس ضرایب و بردار جواب، باید یکسان باشد')
    
    # کنترل حالتی که دستگاه بی‌نهایت جواب داشته باشد
    if A.shape[0] < A.shape[1]:
        return print('دستگاه بی‌نهایت جواب دارد')

    # ساخت ماتریس افزوده
    augmented_matrix = np.hstack((A, b))

    m = A.shape[0] # تعداد سطرها
    n = A.shape[1] # تعداد ستون‌ها

    # اعمال محدودیت برای تعداد ارقام اعداد اعشاری
    np.set_printoptions(precision=2, suppress=True)


    print('# ماتریس افزوده اولیه')
    print(augmented_matrix)

    # حلقه اصلی
    outer_loop = [[0, m - 1, 1], [m - 1, 0, -1]]
    for d in range(2):
        for i in range(outer_loop[d][0], outer_loop[d][1], outer_loop[d][2]):
            inner_loop = [[i + 1, m, 1], [i - 1, -1, -1]]
            for j in range(inner_loop[d][0], inner_loop[d][1], inner_loop[d][2]):
                if augmented_matrix[i, i] != 0:
                    k = (-1) * augmented_matrix[j, i] / augmented_matrix[i, i]
                    temp_row = augmented_matrix[i, :] * k
                    print(f'# Use line{i + 1} for line{j + 1}') # از خطi+1 برای خط j+1استفاده می‌کنیم
                    print(f'k={k}', '*', augmented_matrix[i, :], '=', temp_row)
                    augmented_matrix[j, :] = augmented_matrix[j, :] + temp_row
                    print(augmented_matrix)
                
                elif augmented_matrix[i, i] == 0:
                    if augmented_matrix[i,-1] != 0:
                        print('')
                        return print('دستگاه جواب ندارد')
                    elif augmented_matrix[i, -1] == 0:
                        print('')
                        return print('با قرار دادن Z=a، به بی‌نهایت جواب می‌رسیم')
                    

    for i in range(0, m):
        augmented_matrix[i, :] = augmented_matrix[i, :] / augmented_matrix[i, i]
    print('# اعمال مرحله آخر بر روی سطرها')
    print(augmented_matrix)
    return augmented_matrix[:, n]
        
if __name__ == '__main__':
    A = np.array([[2, 1, 3],
                [4, 3, 5],
                [2, -1, 3]])
    b= np.array([[-2],
                [0],
                [2]])
    A = np.array([[2, 1 , 3],
                [4, 3, 5],
                [6, 5, 7]])
    b= np.array([[1],
                [1],
                [1]])
    Gaussian_Jordan_Elimination(A, b)
