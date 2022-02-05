# Anuneet Anand
# 2018022
# DIP Assignment 4

import cv2
import numpy as np
import matplotlib.pyplot as plt

def LogT(I):
    '''Performs Log Transformation on Image I
    '''
    return np.round((255)*(np.log(1+I)/np.log(1+I.max())))

def F_HSI(pixel):
    ''' Converts RGB Pixel to HSI Pixel
    '''
    r,g,b = pixel/255
    if r == g == b: return [0,0,r]

    o = np.arccos((0.5*((r-g)+(r-b)))/(((r-g)**2+(r-b)*(g-b))**0.5))

    if b <= g:
        h = np.degrees(o)
    else:
        h = np.degrees(2*np.pi - o)

    s = 1 - (3*min(r,g,b))/(r+g+b)
    i = (r+g+b)/3

    HSI_pixel = np.array([h,s,i])
    return HSI_pixel
    
def F_RGB(pixel):
    ''' Converts HSI Pixel to RGB Pixel
    '''
    h,s,i = pixel
    h = np.radians(h)

    if 0 <= h < 2*np.pi/3:
        b = i*(1-s)
        r = i*(1+s*np.cos(h)/(np.cos(np.pi/3-h)))
        g = 3*i - (r+b)

    elif 2*np.pi/3 <= h < 4*np.pi/3:
        h = h - 2*np.pi/3
        r = i*(1-s)
        g = i*(1+s*np.cos(h)/(np.cos(np.pi/3-h)))
        b = 3*i - (r+g)

    else:
        h = h - 4*np.pi/3
        g = i*(1-s)
        b = i*(1+s*np.cos(h)/(np.cos(np.pi/3-h)))
        r = 3*i - (g+b)

    RGB_pixel = np.array([r,g,b])*255
    return RGB_pixel

def A():
    src = "AnuneetAnand_2018022_Image.jpg"
    org = cv2.imread(src,0).astype(np.float64)

    src = "AnuneetAnand_2018022_noiseIm.jpg"
    img = cv2.imread(src,0).astype(np.float64)

    Box_Filter = (1/121) * np.ones((11,11))
    Laplacian_Mask = np.array([[0,1,0],[1,-4,1],[0,1,0]])

    n, m = img.shape
    p, q = Box_Filter.shape
    Lambda_List = {0:[],0.25:[],0.5:[],0.75:[],1.0:[]}
    
    # Padding
    I = np.pad(img,((0,p-1),(0,q-1)),'constant') 
    H = np.pad(Box_Filter,((0,n-1),(0,m-1)),'constant')
    L = np.pad(Laplacian_Mask,((0,n+7),(0,m+7)),'constant')
    
    # Calculating DFTs
    DFT_I = np.fft.fft2(I)
    DFT_H = np.fft.fft2(H)
    DFT_L = np.fft.fft2(L)

    # Trying Different Lambdas
    for Lambda in Lambda_List:
        CLS_F = np.conjugate(DFT_H)/(np.abs(DFT_H)**2+Lambda*np.abs(DFT_L)**2)
        DFT_F = DFT_I*CLS_F
        F = np.fft.ifft2(DFT_F).real
        out = F[0:n,0:m]
        # out = np.round(255*(out-out.min())/(out.max()-out.min()))
        out = out.clip(0,255)
        PSNR = np.round(10*np.log10(255**2/(np.sum((org-out)**2)/(n*m))),3)

        Lambda_List[Lambda].append(PSNR)
        Lambda_List[Lambda].append(CLS_F)
        Lambda_List[Lambda].append(out)

    # Reporting PSNR vs Lambda
    for i in Lambda_List:
        print("Lambda = ", i, "PSNR = ", Lambda_List[i][0])

    Best_Lambda = max(Lambda_List, key=lambda x: Lambda_List[x][0])
    Best_Set = Lambda_List[Best_Lambda]

    # Plotting
    plt.figure()
    plt.suptitle("Constrained Least Square Filtering")
    plt.subplot(2,2,1)
    plt.gca().set_title("Original Image")
    plt.imshow(org.astype(np.uint8),cmap='gray')
    plt.subplot(2,2,2)
    plt.gca().set_title("Noisy Image")
    plt.imshow(img.astype(np.uint8),cmap='gray')
    plt.subplot(2,2,3)
    plt.gca().set_title("Best Restored Image"+"\n"+"(Lambda = "+str(Best_Lambda)+", PSNR = "+str(Best_Set[0])+")")
    plt.imshow(Best_Set[2].astype(np.uint8),cmap='gray')
    plt.subplot(2,2,4)
    plt.gca().set_title("CLS Filter (Centered)")
    plt.imshow(LogT(np.abs(np.fft.fftshift(Best_Set[1]))),cmap='gray')
    plt.tight_layout()

def B():
    src = "AnuneetAnand_2018022_rgbIm.tif"
    img = (cv2.imread(src)[:,:,::-1]).astype(np.float64)
    m, n, _ = img.shape

    # Converting to HSI
    img_HSI = np.zeros(img.shape)
    for i in range(m):
        for j in range(n):
            img_HSI[i][j] = F_HSI(img[i][j])

    # Performing Histogram Equalization on I
    img_I = np.round(img_HSI[:,:,2]*255)
    hist = np.array([(img_I==i).sum()/(m*n) for i in range(256)])
    transform = np.round(hist.cumsum()*255)
    
    out_I = img_I.copy()
    for i in range(256):
        out_I[np.where(img_I==i)] = transform[i]
    
    eq_hist = np.array([(out_I==i).sum()/(m*n) for i in range(256)])
    out_HSI = img_HSI.copy()
    out_HSI[:,:,2] = out_I/255

    # Converting to RGB
    out = np.zeros(img.shape)
    for i in range(m):
        for j in range(n):
            out[i][j] = F_RGB(out_HSI[i][j])
    
    # out = np.round(255*(out-out.min())/(out.max()-out.min()))
    out = out.clip(0,255)

    # Plotting
    plt.figure()
    plt.suptitle("Histogram Equalization in HSI Space")
    plt.subplot(2,2,1)
    plt.gca().set_title("Original RGB Image")
    plt.imshow(img/255)
    plt.subplot(2,2,2)
    plt.gca().set_title("Normalised Intensity Channel Histogram of Orginal Image")
    plt.bar([i for i in range(256)],hist)
    plt.subplot(2,2,3)
    plt.gca().set_title("Equalized RGB Image")
    plt.imshow(out/255)
    plt.subplot(2,2,4)
    plt.gca().set_title("Normalised Intensity Channel Histogram of Equalized Image")
    plt.bar([i for i in range(256)],eq_hist)
    plt.tight_layout()

if __name__ == "__main__":
    A()
    B()
    plt.show()