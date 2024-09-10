import math
import cv2
import numpy as np
import Preprocess

def detect_license_plate(image_path):
    n = 1

    Min_char = 0.01
    Max_char = 0.09

    RESIZED_IMAGE_WIDTH = 20
    RESIZED_IMAGE_HEIGHT = 30

    first_line = ""  # Khởi tạo biến first_line
    second_line = ""  # Khởi tạo biến second_line
    img = cv2.imread(image_path)

    ######## Upload KNN model ######################
    npaClassifications = np.loadtxt("classificationS.txt", np.float32)
    npaFlattenedImages = np.loadtxt("flattened_images.txt", np.float32)
    npaClassifications = npaClassifications.reshape(
        (npaClassifications.size, 1))  # reshape numpy array to 1d, necessary to pass to call to train
    kNearest = cv2.ml.KNearest_create()  # instantiate KNN object
    kNearest.train(npaFlattenedImages, cv2.ml.ROW_SAMPLE, npaClassifications)
    #########################

    ################ Image Preprocessing #################
    imgGrayscaleplate, imgThreshplate = Preprocess.preprocess(img)
    canny_image = cv2.Canny(imgThreshplate, 250, 255)  # Canny Edge
    kernel = np.ones((3, 3), np.uint8)
    dilated_image = cv2.dilate(canny_image, kernel, iterations=1)  # Dilation
    # cv2.imshow("dilated_image",dilated_image)

    ###########################################

    ###### Draw contour and filter out the license plate  #############
    contours, hierarchy = cv2.findContours(dilated_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:2]  # Sắp xếp giảm dần và lấy 2 contours có diện tích lớn nhất
    # cv2.drawContours(img, contours, -1, (255, 0, 255), 3) # Vẽ tất cả các ctour trong hình lớn

    screenCnt = []
    for c in contours:
        peri = cv2.arcLength(c, True)  # Tính chu vi contours
        approx = cv2.approxPolyDP(c, 0.06 * peri, True)  # làm xấp xỉ contours thành đa giác có số cạnh ít hơn, 
        [x, y, w, h] = cv2.boundingRect(approx.copy())
        ratio = w / h
        # cv2.putText(img, str(len(approx.copy())), (x,y),cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 0), 3)
        # cv2.putText(img, str(ratio), (x,y),cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 0), 3)
        if (len(approx) == 4):
            screenCnt.append(approx)
        #chỉ giữ contour có 4 cạnh
            #cv2.putText(img, str(len(approx.copy())), (x, y), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 0), 3)

    if screenCnt is None:
        detected = 0
        print("No plate detected")
    else:
        detected = 1

    if detected == 1:

        for screenCnt in screenCnt:
            #cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)  # Khoanh vùng biển số xe

            ############## Find the angle of the license plate #####################
            (x1, y1) = screenCnt[0, 0]
            (x2, y2) = screenCnt[1, 0]
            (x3, y3) = screenCnt[2, 0]
            (x4, y4) = screenCnt[3, 0]
            array = [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
            sorted_array = array.sort(reverse=True, key=lambda x: x[1])
            (x1, y1) = array[0]
            (x2, y2) = array[1]
            #Tính khoảng cách theo trục y (độ chênh lệch chiều cao) giữa hai điểm, lưu vào biến doi.
            #Tính khoảng cách theo trục x (độ chênh lệch chiều ngang) giữa hai điểm, lưu vào biến ke.
            doi = abs(y1 - y2)
            ke = abs(x1 - x2)
            '''
            Sử dụng hàm atan (arc tangent) để tính góc giữa cạnh ngang và trục x của biển số. math.atan(doi / ke) tính góc theo radian.
            Nhân giá trị này với (180.0 / math.pi) để chuyển đổi từ radian sang độ.
            Tính góc nghiêng của biến số
            '''
            angle = math.atan(doi / ke) * (180.0 / math.pi)

            ####################################

            ########## Crop out the license plate and align it to the right angle ################

            mask = np.zeros(imgGrayscaleplate.shape, np.uint8)
            new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1, )
            # cv2.imshow("new_image",new_image)

            # Cropping
            (x, y) = np.where(mask == 255)
            (topx, topy) = (np.min(x), np.min(y)) #tọa độ trên cùng bên trái của vùng chứa biển số.
            (bottomx, bottomy) = (np.max(x), np.max(y)) #tọa độ dưới cùng bên phải của vùng chứa biển số.

            roi = img[topx:bottomx, topy:bottomy] #vùng cắt (region of interest) từ ảnh gốc img chứa biển số xe.
            imgThresh = imgThreshplate[topx:bottomx, topy:bottomy] #vùng cắt tương ứng từ ảnh ngưỡng imgThreshplate.
            ptPlateCenter = (bottomx - topx) / 2, (bottomy - topy) / 2 #tâm của vùng biển số xe (sử dụng để làm điểm xoay).

            #Kiểm tra xem điểm (x1, y1) có nằm bên trái điểm (x2, y2) hay không.
            #Nếu đúng, tạo ma trận xoay rotationMatrix với góc -angle để xoay ngược chiều kim đồng hồ (đưa biển số về nằm ngang).
            #Nếu không, tạo ma trận xoay với góc angle để xoay thuận chiều kim đồng hồ.
                        
            if x1 < x2:
                rotationMatrix = cv2.getRotationMatrix2D(ptPlateCenter, -angle, 1.0)
            else:
                rotationMatrix = cv2.getRotationMatrix2D(ptPlateCenter, angle, 1.0)

            roi = cv2.warpAffine(roi, rotationMatrix, (bottomy - topy, bottomx - topx)) #áp dụng ma trận xoay rotationMatrix lên roi và imgThresh, xoay cả hai hình ảnh để biển số nằm ngang.
            imgThresh = cv2.warpAffine(imgThresh, rotationMatrix, (bottomy - topy, bottomx - topx))
            roi = cv2.resize(roi, (0, 0), fx=3, fy=3) #phóng to roi và imgThresh với hệ số fx=3 và fy=3 để dễ dàng nhận diện ký tự sau này.
            imgThresh = cv2.resize(imgThresh, (0, 0), fx=3, fy=3)

            ####################################

            #################### Prepocessing and Character segmentation ####################
            kerel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            thre_mor = cv2.morphologyEx(imgThresh, cv2.MORPH_DILATE, kerel3)
            cont, hier = cv2.findContours(thre_mor, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            #cv2.imshow(str(n + 20), thre_mor)
            #cv2.drawContours(roi, cont, -1, (100, 255, 255), 2)  # Vẽ contour các kí tự trong biển số

            ##################### Filter out characters #################
            char_x_ind = {} #từ điển để lưu vị trí x của các ký tự và chỉ số contour tương ứng.
            char_x = [] #danh sách để lưu trữ tọa độ x của các ký tự.
            height, width, _ = roi.shape #chiều cao và chiều rộng của vùng cắt (ROI).
            roiarea = height * width #diện tích của ROI, dùng để tính toán tỷ lệ diện tích của các ký tự.

            for ind, cnt in enumerate(cont):
                (x, y, w, h) = cv2.boundingRect(cont[ind])
                ratiochar = w / h
                char_area = w * h
                # cv2.putText(roi, str(char_area), (x, y+20),cv2.FONT_HERSHEY_DUPLEX, 2, (255, 255, 0), 2)
                # cv2.putText(roi, str(ratiochar), (x, y+20),cv2.FONT_HERSHEY_DUPLEX, 2, (255, 255, 0), 2)

                if (Min_char * roiarea < char_area < Max_char * roiarea) and (0.25 < ratiochar < 0.7):
                    if x in char_x:  # Sử dụng để dù cho trùng x vẫn vẽ được
                        x = x + 1
                    char_x.append(x)
                    char_x_ind[x] = ind

                    # cv2.putText(roi, str(char_area), (x, y+20),cv2.FONT_HERSHEY_DUPLEX, 2, (255, 255, 0), 2)

            '''Đoạn mã này thực hiện việc tiền xử lý và tìm các contour đại diện cho các ký tự trong vùng biển số xe. 
            Nó sử dụng các phép toán hình thái học để làm dày các ký tự, tìm các contour và lọc ra các contour có 
            kích thước và tỷ lệ phù hợp với các ký tự. 
            Các tọa độ x của các ký tự được lưu trữ để sử dụng trong bước nhận dạng ký tự sau này.'''
            ############ Character recognition ##########################

            char_x = sorted(char_x) #sắp xếp danh sách các tọa độ x của các ký tự theo thứ tự tăng dần.
            strFinalString = ""
            first_line = ""
            second_line = ""

            for i in char_x:
                (x, y, w, h) = cv2.boundingRect(cont[char_x_ind[i]])
                cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)

                imgROI = thre_mor[y:y + h, x:x + w]  # Crop the characters

                imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))  #  thay đổi kích thước ảnh chứa ký tự về kích thước chuẩn (20x30).
                npaROIResized = imgROIResized.reshape(
                    (1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT)) #chuyển đổi ảnh về dạng mảng 1 chiều.

                npaROIResized = np.float32(npaROIResized) #chuyển đổi mảng về kiểu dữ liệu float32.
                _, npaResults, neigh_resp, dists = kNearest.findNearest(npaROIResized,k=3)  # ử dụng mô hình KNN để nhận dạng ký tự từ ảnh đã được tiền xử lý. k=3 nghĩa là sử dụng 3 hàng xóm gần nhất để quyết định ký tự.
                strCurrentChar = str(chr(int(npaResults[0][0])))  #  chuyển đổi kết quả nhận dạng (mã ASCII) thành ký tự.
                cv2.putText(roi, strCurrentChar, (x, y + 50), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 255, 0), 3) #vẽ ký tự nhận dạng được lên ảnh vùng biển số xe (ROI).

                if (y < height / 3):  # Nếu nằm trong 1/3 ảnh phía trên thì là dòng số 1 của biển, còn lại thì là dòng 2
                    first_line = first_line + strCurrentChar
                else:
                    second_line = second_line + strCurrentChar

            #print("\n License Plate " + str(n) + " is: " + first_line + second_line + "\n")
            roi = cv2.resize(roi, None, fx=0.75, fy=0.75)
            #cv2.imshow(str(n), cv2.cvtColor(roi, cv2.COLOR_BGR2RGB))

        return first_line + second_line  # Trả về giá trị của biển số

    return None, None  # Trả về None nếu không tìm thấy biển số

# Sử dụng hàm để nhận diện biển số
#first_line, second_line = detect_license_plate("16.jpg")
#license_plate_text = first_line + second_line  # Kết hợp hai dòng thành một chuỗi
#print("Detected License Plate:", license_plate_text)
