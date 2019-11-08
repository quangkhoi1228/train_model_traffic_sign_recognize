{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "import cv2\n",
    "import math\n",
    "\n",
    "def rgb_select(img, thresh=(0, 255)):\n",
    "    R = img[:,:,2] \n",
    "    G = img[:,:,1]\n",
    "    B = img[:,:,0]\n",
    "    binary_output = np.zeros_like(R)\n",
    "    binary_output[(R >= thresh[0]) & (R <= thresh[1]) & (G >= thresh[0]) & (G <= thresh[1]) & (B >= thresh[0]) & (B <= thresh[1])] = 1\n",
    "    return binary_output\n",
    "\n",
    "def line_in_shadow(img, thresh1=(0,255),thresh2=(0,255),thresh3=(0,255)):\n",
    "    R = img[:,:,2] \n",
    "    G = img[:,:,1]\n",
    "    B = img[:,:,0]\n",
    "    # Return a binary image of threshold result\n",
    "    binary_output = np.zeros_like(R)\n",
    "    binary_output[(R >= thresh1[0]) & (R <= thresh1[1]) & (G >= thresh2[0]) & (G <= thresh2[1]) & (B >= thresh3[0]) & (B <= thresh3[1])] = 1\n",
    "    return binary_output\n",
    "\n",
    "def binary_pipeline(img):\n",
    "    img_copy = cv2.GaussianBlur(img, (3, 3), 0)\n",
    "    red_binary = rgb_select(img_copy, thresh=(200,255))\n",
    "    line_shadow = line_in_shadow(img_copy,thresh1=(50,90),thresh2=(60,120),thresh3=(120,150))\n",
    "    binary =  cv2.bitwise_or(line_shadow,red_binary)\n",
    "    return binary\n",
    "\n",
    "\n",
    "def hsv_select(img, lower=np.array([10, 0, 0]), upper =np.array([180, 50,210])):\n",
    "    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)\n",
    "    mask = cv2.inRange(hsv_img, lower, upper)\n",
    "    # cv2.imshow(\"mask\", hsv_img)\n",
    "    return mask\n",
    "\n",
    "def lane_in_shadow(img, lower=np.array([45, 55, 60]), upper =np.array([55, 70,80])):\n",
    "    R = img[:,:,2] \n",
    "    G = img[:,:,1]\n",
    "    B = img[:,:,0]\n",
    "    binary_output = np.zeros_like(R)\n",
    "    binary_output[(R >= lower[0]) & (R <= upper[0]) & (G >= lower[1]) & (G <= upper[1]) & (B >= lower[2]) & (B <= upper[2])] = 255\n",
    "    # cv2.imshow(\"hsv_img\", img)\n",
    "    return binary_output\n",
    "\n",
    "def warp_image(img):\n",
    "    \n",
    "    image_size = (img.shape[1], img.shape[0])\n",
    "    x = img.shape[1]\n",
    "    y = img.shape[0]\n",
    "\n",
    "    #the \"order\" of points in the polygon you are defining does not matter\n",
    "    #but they need to match the corresponding points in destination_points!\n",
    "    ## my source\n",
    "    source_points = np.float32([\n",
    "    [0, y],\n",
    "    [0, (7/9)*y+10],\n",
    "    [x, (7/9)*y+10],\n",
    "    [x, y]\n",
    "    ])\n",
    "    \n",
    "    destination_points = np.float32([\n",
    "    [0.25 * x, y],\n",
    "    [0.25 * x, 0],\n",
    "    [x - (0.25 * x), 0],\n",
    "    [x - (0.25 * x), y]\n",
    "    ])\n",
    "    \n",
    "    perspective_transform = cv2.getPerspectiveTransform(source_points, destination_points)\n",
    "    inverse_perspective_transform = cv2.getPerspectiveTransform( destination_points, source_points)\n",
    "    \n",
    "    warped_img = cv2.warpPerspective(img, perspective_transform, image_size, flags=cv2.INTER_LINEAR)\n",
    "\n",
    "    return warped_img, inverse_perspective_transform\n",
    "\n",
    "def get_val(y,poly_coeff):\n",
    "    return poly_coeff[0]*y**2+poly_coeff[1]*y+poly_coeff[2]\n",
    "\n",
    "def check_lane_inds(left_lane_inds, right_lane_inds):\n",
    "    countleft = 0\n",
    "    countright = 0\n",
    "    missing_one_line = False\n",
    "    for x in range(9):\n",
    "        left = np.asarray(left_lane_inds[x])\n",
    "        right = np.asarray(right_lane_inds[x])\n",
    "        if len(left) == 0:\n",
    "            countleft+=1\n",
    "        if len(right) == 0:\n",
    "            countright+=1\n",
    "        if len(left) == len(right) and len(left) !=0 and len(right) != 0:\n",
    "            if (left == right).all():\n",
    "                missing_one_line = True\n",
    "    if missing_one_line:\n",
    "        if countleft == countright:\n",
    "            return left_lane_inds, right_lane_inds\n",
    "        if countleft < countright:\n",
    "            return left_lane_inds, []\n",
    "        return [], right_lane_inds\n",
    "    if countleft >= 6:\n",
    "        return [], right_lane_inds\n",
    "    if countright >= 6:\n",
    "        return left_lane_inds, []\n",
    "    return left_lane_inds,right_lane_inds\n",
    "\n",
    "def track_lanes_initialize(binary_warped):   \n",
    "    histogram = np.sum(binary_warped[int(binary_warped.shape[0]/2):,:], axis=0)\n",
    "    out_img = np.dstack((binary_warped, binary_warped, binary_warped))\n",
    "    midpoint = np.int(histogram.shape[0]/2)\n",
    "    leftx_base = np.argmax(histogram[:midpoint+100])\n",
    "    rightx_base = np.argmax(histogram[midpoint+100:]) + midpoint+100\n",
    "    nwindows = 9\n",
    "    window_height = np.int(binary_warped.shape[0]/nwindows)\n",
    "    nonzero = binary_warped.nonzero()\n",
    "    nonzeroy = np.array(nonzero[0])\n",
    "    nonzerox = np.array(nonzero[1])\n",
    "    leftx_current = leftx_base\n",
    "    rightx_current = rightx_base\n",
    "    # Set the width of the windows +/- margin\n",
    "    margin = 100\n",
    "    # Set minimum number of pixels found to recenter window\n",
    "    minpix = 60\n",
    "    # Create empty lists to receive left and right lane pixel indices\n",
    "    left_lane_inds = []\n",
    "    right_lane_inds = []  \n",
    "    for window in range(nwindows):\n",
    "        # Identify window boundaries in x and y (and right and left)\n",
    "        win_y_low = int(binary_warped.shape[0] - (window+1)*window_height)\n",
    "        win_y_high = int(binary_warped.shape[0] - window*window_height)\n",
    "        win_xleft_low = leftx_current - margin\n",
    "        win_xleft_high = leftx_current + margin\n",
    "        win_xright_low = rightx_current - margin\n",
    "        win_xright_high = rightx_current + margin\n",
    "        # Draw the windows on the visualization image\n",
    "        cv2.rectangle(out_img,(win_xleft_low,win_y_low),(win_xleft_high,win_y_high),(0,255,0), 3) \n",
    "        cv2.rectangle(out_img,(win_xright_low,win_y_low),(win_xright_high,win_y_high),(0,255,0), 3) \n",
    "        # cv2.imshow('out_img',out_img)\n",
    "        # Identify the nonzero pixels in x and y within the window\n",
    "        good_left_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xleft_low) & (nonzerox < win_xleft_high)).nonzero()[0]\n",
    "        good_right_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xright_low) & (nonzerox < win_xright_high)).nonzero()[0]\n",
    "        # Append these indices to the lists\n",
    "        \n",
    "        left_lane_inds.append(good_left_inds)\n",
    "        right_lane_inds.append(good_right_inds)\n",
    "        # If you found > minpix pixels, recenter next window on their mean position\n",
    "        if len(good_left_inds) > minpix:\n",
    "            leftx_current = np.int(np.mean(nonzerox[good_left_inds]))\n",
    "        if len(good_right_inds) > minpix:        \n",
    "            rightx_current = np.int(np.mean(nonzerox[good_right_inds]))\n",
    "        \n",
    "    \n",
    "    left_lane_inds,right_lane_inds = check_lane_inds(left_lane_inds,right_lane_inds)\n",
    "    if len(left_lane_inds) != 0:\n",
    "        left_lane_inds = np.concatenate(left_lane_inds)\n",
    "    if len(right_lane_inds) !=0:\n",
    "        right_lane_inds = np.concatenate(right_lane_inds)\n",
    "    leftx = nonzerox[left_lane_inds]\n",
    "    lefty = nonzeroy[left_lane_inds] \n",
    "    rightx = nonzerox[right_lane_inds]\n",
    "    righty = nonzeroy[right_lane_inds] \n",
    "    left_fit = np.array([])\n",
    "    right_fit = np.array([])\n",
    "    if len(leftx) != 0:\n",
    "        left_fit  = np.polyfit(lefty, leftx, 2)\n",
    "    if len(rightx) != 0:\n",
    "        right_fit  = np.polyfit(righty, rightx, 2)\n",
    "    return left_fit, right_fit\n",
    "\n",
    "def check_fit_duplication(left_fit, right_fit):\n",
    "    if len(left_fit) == 0 or len(right_fit) == 0:\n",
    "        return left_fit, right_fit\n",
    "    # print(left_fit[2], right_fit[2])\n",
    "    if abs(left_fit[0] - right_fit[0]) < 0.1:\n",
    "        if abs(left_fit[1] - right_fit[1]) < 0.4:\n",
    "            if abs(left_fit[2] - right_fit[2]) < 30:\n",
    "                return left_fit, []\n",
    "    return left_fit, right_fit\n",
    "\n",
    "\n",
    "#### UPDATE #####\n",
    "def get_point_in_lane(image):\n",
    "    warp,_ = warp_image(image)\n",
    "    lane_image = hsv_select(warp)\n",
    "    lane_shadow = lane_in_shadow(warp)\n",
    "    lane = cv2.bitwise_or(lane_image,lane_shadow)\n",
    "    # cv2.imshow('lane_image',lane)\n",
    "    histogram_x = np.sum(lane[:,:], axis=0)\n",
    "    histogram_y = np.sum(lane[:,:], axis=1)\n",
    "    lane_x = np.argmax(histogram_x)\n",
    "    lane_y = np.argmax(histogram_y)\n",
    "    for y in range(lane_y,0,-1):\n",
    "        if lane[y][lane_x] == 255:\n",
    "            return [y, lane_x]\n",
    "    return 0,0\n",
    "\n",
    "def find_center_line_for_missing_one_line(image,left_fit,right_fit):\n",
    "    ploty = np.linspace(0, image.shape[0]-1, image.shape[0])\n",
    "    point_in_lane = get_point_in_lane(image)\n",
    "    avaiable_fit =  left_fit\n",
    "    center_x = np.array([])\n",
    "    if len(left_fit) == 0:\n",
    "        avaiable_fit = right_fit\n",
    "    val = point_in_lane[1] - get_val(point_in_lane[0],avaiable_fit)\n",
    "    if val > 0:\n",
    "        print(\"missing right line\")\n",
    "        #left avaiable\n",
    "        left_fitx = get_val(ploty,avaiable_fit)\n",
    "        # max image.shape[1]*0.25+1, min image.shape[1]-image.shape[1]*0.3-1\n",
    "        center_x = np.clip(left_fitx+150,image.shape[1]*0.25+1,image.shape[1]-image.shape[1]*0.25-1)\n",
    "        left_fit = avaiable_fit\n",
    "        right_fit = np.array([])\n",
    "    else:\n",
    "        print(\"missing left line\")\n",
    "        #right avaiable\n",
    "        right_fitx = get_val(ploty,avaiable_fit)\n",
    "        center_x = np.clip(right_fitx-150,image.shape[1]*0.25+1,image.shape[1]-image.shape[1]*0.25-1)\n",
    "        right_fit = avaiable_fit\n",
    "        left_fit = np.array([])\n",
    "    center_fit = np.polyfit(ploty, center_x, 2)\n",
    "    return center_fit, left_fit, right_fit\n",
    "\n",
    "def find_center_line_and_update_fit(image,left_fit,right_fit):\n",
    "    if len(left_fit) == 0  and len(right_fit) == 0: # missing 2 line:\n",
    "        center_fit =  np.array([0,0,image.shape[1]/2])\n",
    "        left_fit_update = np.array([])\n",
    "        right_fit_update = np.array([])\n",
    "        return center_fit, left_fit_update, right_fit_update\n",
    "    if len(left_fit) == 0 or len(right_fit) == 0: #missing 1 line\n",
    "        center_fit, left_fit_update, right_fit_update = find_center_line_for_missing_one_line(image,left_fit,right_fit)\n",
    "        return center_fit, left_fit_update, right_fit_update\n",
    "    # none missing line\n",
    "    ploty = np.linspace(0, image.shape[0]-1, image.shape[0])\n",
    "    leftx = get_val(ploty, left_fit)\n",
    "    rightx = get_val(ploty, right_fit)\n",
    "    center_x = (leftx+rightx)/2\n",
    "    center_fit = np.polyfit(ploty, center_x, 2)\n",
    "    return center_fit, left_fit, right_fit\n",
    "\n",
    "def lane_fill_poly(binary_warped,undist,center_fit,left_fit,right_fit, inverse_perspective_transform):\n",
    "    ploty = np.linspace(0, binary_warped.shape[0]-1, binary_warped.shape[0])\n",
    "    if len(left_fit) == 0:\n",
    "        left_fit = np.array([0,0,1])\n",
    "    if len(right_fit) == 0:\n",
    "        right_fit = np.array([0,0,binary_warped.shape[1]-1])\n",
    "    left_fitx = get_val(ploty,left_fit)\n",
    "    right_fitx = get_val(ploty,right_fit)\n",
    "    center_fitx = get_val(ploty,center_fit)\n",
    "    # Create an image to draw the lines on\n",
    "    warp_zero = np.zeros_like(binary_warped).astype(np.uint8)\n",
    "    color_warp = np.dstack((warp_zero, warp_zero, warp_zero))\n",
    "    center_color_warp = np.dstack((warp_zero, warp_zero, warp_zero))\n",
    "    # Recast x and y for cv2.fillPoly()\n",
    "    pts_left = np.array([np.transpose(np.vstack([left_fitx, ploty]))])\n",
    "    pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, ploty])))])\n",
    "    pts_center = np.array([np.transpose(np.vstack([center_fitx, ploty]))])\n",
    "    pts = np.hstack((pts_left, pts_right))\n",
    "    # Draw the lane \n",
    "    cv2.fillPoly(color_warp, np.int_([pts]), (0,255, 0))\n",
    "    cv2.fillPoly(center_color_warp, np.int_([pts_center]),(0,0,255))\n",
    "    # Warp using inverse perspective transform\n",
    "    newwarp = cv2.warpPerspective(color_warp, inverse_perspective_transform, (binary_warped.shape[1], binary_warped.shape[0])) \n",
    "    center_line = cv2.warpPerspective(center_color_warp, inverse_perspective_transform, (binary_warped.shape[1], binary_warped.shape[0])) \n",
    "   \n",
    "    result = cv2.addWeighted(undist, 1, newwarp, 0.7, 0.3)\n",
    "    result = cv2.addWeighted(result,1,center_line,0.7,0.3)\n",
    "    return result, center_line\n",
    "\n",
    "############################## calcul steer angle #############################\n",
    "def find_point_center(center_line):\n",
    "    roi = int(center_line.shape[0]*(7/9))+10\n",
    "    for y in range(roi,center_line.shape[0]):\n",
    "        for x in range(center_line.shape[1]):\n",
    "            if center_line[y][x][2] == 255:\n",
    "                cv2.circle(center_line,(x,y),1,(255,0,0),7)\n",
    "                # cv2.imshow('center_point',center_line)\n",
    "                return x,y\n",
    "    return 0,0\n",
    "\n",
    "def errorAngle(center_line):\n",
    "    carPosx , carPosy = 320, 480\n",
    "    dstx, dsty = find_point_center(center_line)\n",
    "    # print(carPosx,carPosy)\n",
    "    if dstx == carPosx:\n",
    "        return 0\n",
    "    if dsty == carPosy:\n",
    "        if dstx < carPosx:\n",
    "            return -45\n",
    "        else:\n",
    "            return 45\n",
    "    pi = math.acos(-1.0)\n",
    "    dx = dstx - carPosx\n",
    "    dy = carPosy - dsty\n",
    "    if dx < 0: \n",
    "        angle = (math.atan(-dx / dy) * -180 / pi)/2.5\n",
    "        if angle >= 28 or angle <= -28: # maybe must turn 90\n",
    "            if angle > 0:\n",
    "                return 45\n",
    "            return -45\n",
    "        return angle\n",
    "    #################################################\n",
    "    angle = (math.atan(dx / dy) * 180 / pi)/2.5\n",
    "    if angle >= 25 or angle <= -25: # maybe must turn 90\n",
    "        if angle > 0:\n",
    "            return 45\n",
    "        return -45\n",
    "    return angle\n",
    "\n",
    "def calcul_speed(steer_angle):\n",
    "    max_speed = 70\n",
    "    max_angle = 40\n",
    "    if steer_angle == -45 or steer_angle == 45:\n",
    "        return 0\n",
    "    if steer_angle >= 4 or steer_angle <= -4:\n",
    "        if steer_angle > 0:\n",
    "            return max_speed - (max_speed/max_angle)*steer_angle\n",
    "        else:\n",
    "            return max_speed + (max_speed/max_angle)*steer_angle \n",
    "    elif steer_angle >= 15 or steer_angle <= -15:\n",
    "        if steer_angle > 0:\n",
    "            return 40 - (40/max_angle)*steer_angle\n",
    "        else:\n",
    "            return 40 + (30/max_angle)*steer_angle\n",
    "    # elif steer_angle >= 10 or steer_angle <= -10:\n",
    "    #     if steer_angle > 0:\n",
    "    #         return max_speed - (max_speed/max_angle)*steer_angle\n",
    "    #     else:\n",
    "    #         return max_speed + (max_speed/max_angle)*steer_angle \n",
    "    # if steer_angle >=0:\n",
    "    #     return max_speed - (max_speed/max_angle)*steer_angle\n",
    "    return max_speed \n",
    "################## find line avaiable ######################\n",
    "# def line_processing(image):\n",
    "#    binary_image =  binary_pipeline(image)\n",
    "#    bird_view, inverse_perspective_transform =  warp_image(binary_image)\n",
    "#    left_fit, right_fit = track_lanes_initialize(bird_view)\n",
    "#    return left_fit, right_fit,bird_view, inverse_perspective_transform\n",
    "################## Draw lane avaiable #######################\n",
    "# def draw_lane(image, bird_view, left_fit, right_fit, inverse_perspective_transform):\n",
    "#     left_fit, right_fit = check_fit_duplication(left_fit,right_fit)\n",
    "#     center_fit, left_fit, right_fit = find_center_line_and_update_fit(image,left_fit,right_fit) # update left, right line\n",
    "#     colored_lane, center_line = lane_fill_poly(bird_view,image,center_fit,left_fit,right_fit, inverse_perspective_transform)\n",
    "#     cv2.imshow(\"lane\",colored_lane)\n",
    "#     return center_line\n",
    "def get_speed_angle(center_line):\n",
    "#    # calculate speed and angle\n",
    "   steer_angle =  errorAngle(center_line)\n",
    "   speed_current = calcul_speed(steer_angle)\n",
    "   return speed_current, steer_angle"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}