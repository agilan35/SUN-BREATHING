"""
Image Processing Pipeline for Certificate & Document Visual Inspection
Using OpenCV and NumPy for anomaly detection
"""

import os
import sys
import cv2
import numpy as np
from pathlib import Path
import hashlib

# Configure safe output encoding for Windows
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass


class ImageProcessor:
    """Analyzes document images for visual anomalies and fraud indicators"""

    def __init__(self):
        self.blur_threshold = 100  # Laplacian variance threshold for blur detection
        self.edge_threshold = 0.15  # Threshold for edge consistency
        self.color_consistency_threshold = 0.2  # For color anomalies

    def load_image(self, image_path):
        """Load image from file path with support for Windows and unicode paths"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at {image_path}")
        
        # Read via numpy buffer for robustness on Windows unicode paths
        try:
            with open(image_path, 'rb') as f:
                bytes_data = bytearray(f.read())
                numpy_array = np.asarray(bytes_data, dtype=np.uint8)
                image = cv2.imdecode(numpy_array, cv2.IMREAD_COLOR)
        except Exception:
            image = cv2.imread(image_path)

        if image is None:
            raise ValueError(f"Could not decode image from {image_path}")
        return image

    def get_image_hash(self, image_path):
        """Generate SHA256 hash of image for verification logging"""
        with open(image_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()

    def check_blur_quality(self, image):
        """
        Detect image blur using Laplacian variance method
        Higher variance = sharper image, Lower variance = blurry image
        Returns: (is_sharp: bool, variance: float, blur_score: float)
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        laplacian_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())
        
        is_sharp = laplacian_var > self.blur_threshold
        blur_score = min(100.0, (laplacian_var / max(self.blur_threshold, 1.0)) * 100.0)
        
        return is_sharp, laplacian_var, blur_score

    def detect_copy_paste_artifacts(self, image):
        """
        Detect copy-paste regions using edge consistency analysis
        Returns: (has_artifacts: bool, artifact_score: float)
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        
        edge_variance = float(np.var(closed))
        edge_mean = float(np.mean(closed))
        
        if edge_mean == 0:
            consistency_score = 0.0
        else:
            consistency_score = min(100.0, (edge_variance / (edge_mean + 1.0)) * 50.0)
        
        has_artifacts = consistency_score > 40.0
        return has_artifacts, consistency_score

    def detect_pixel_anomalies(self, image):
        """
        Detect suspicious pixel patterns (editing, compression anomalies)
        Returns: (has_anomalies: bool, anomaly_score: float)
        """
        ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
        y, cr, cb = cv2.split(ycrcb)
        
        y_hist = cv2.calcHist([y], [0], None, [256], [0, 256])
        max_bin = float(np.max(y_hist))
        total_pixels = float(y.size)
        histogram_concentration = max_bin / max(total_pixels, 1.0)
        
        anomaly_score = min(100.0, histogram_concentration * 1000.0)
        has_anomalies = anomaly_score > 35.0
        
        return has_anomalies, anomaly_score

    def detect_gradient_inconsistencies(self, image):
        """
        Detect gradient/lighting inconsistencies suggesting tampering
        Returns: (has_inconsistencies: bool, inconsistency_score: float)
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
        magnitude = np.sqrt(sobelx**2 + sobely**2)
        
        h, w = magnitude.shape
        h_half, w_half = max(h // 2, 1), max(w // 2, 1)
        
        quadrants = [
            magnitude[:h_half, :w_half],
            magnitude[:h_half, w_half:],
            magnitude[h_half:, :w_half],
            magnitude[h_half:, w_half:]
        ]
        
        means = [float(np.mean(q)) for q in quadrants if q.size > 0]
        std_of_means = float(np.std(means)) if means else 0.0
        
        inconsistency_score = min(100.0, std_of_means * 5.0)
        has_inconsistencies = inconsistency_score > 25.0
        
        return has_inconsistencies, inconsistency_score

    def detect_compression_artifacts(self, image):
        """
        Detect JPEG compression artifacts or other digital tampering
        Returns: (has_compression_artifacts: bool, compression_score: float)
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        dct_blocks = []
        
        step = 8
        for i in range(0, max(gray.shape[0] - step, 1), step):
            for j in range(0, max(gray.shape[1] - step, 1), step):
                block = gray[i:i+step, j:j+step].astype(np.float32)
                if block.shape == (8, 8):
                    dct = cv2.dct(block)
                    high_freq = float(np.sum(np.abs(dct[1:, 1:])))
                    dct_blocks.append(high_freq)
        
        if len(dct_blocks) > 0:
            mean_dct = float(np.mean(dct_blocks))
            std_dct = float(np.std(dct_blocks))
            compression_score = min(100.0, (std_dct / (mean_dct + 1.0)) * 20.0)
        else:
            compression_score = 0.0
        
        has_artifacts = compression_score > 35.0
        return has_artifacts, compression_score

    def analyze_text_region_consistency(self, image):
        """
        Analyze consistency of text regions (font, spacing, alignment)
        Returns: (is_consistent: bool, consistency_score: float)
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) < 5:
            return False, 30.0
        
        heights = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if 5 < h < 200:
                heights.append(float(h))
        
        if len(heights) > 0:
            height_variance = float(np.std(heights)) / (float(np.mean(heights)) + 1.0)
            consistency_score = max(0.0, min(100.0, 100.0 - (height_variance * 50.0)))
        else:
            consistency_score = 50.0
        
        is_consistent = consistency_score > 60.0
        return is_consistent, consistency_score

    def comprehensive_visual_analysis(self, image_path):
        """
        Perform comprehensive visual inspection of document
        Returns: detailed analysis report
        """
        image = self.load_image(image_path)
        image_hash = self.get_image_hash(image_path)
        
        is_sharp, blur_variance, blur_score = self.check_blur_quality(image)
        has_copy_paste, copy_paste_score = self.detect_copy_paste_artifacts(image)
        has_pixel_anomalies, pixel_anomaly_score = self.detect_pixel_anomalies(image)
        has_gradient_issues, gradient_score = self.detect_gradient_inconsistencies(image)
        has_compression, compression_score = self.detect_compression_artifacts(image)
        is_text_consistent, text_consistency_score = self.analyze_text_region_consistency(image)
        
        anomaly_scores = [
            (100.0 - copy_paste_score) if has_copy_paste else 100.0,
            (100.0 - pixel_anomaly_score) if has_pixel_anomalies else 100.0,
            (100.0 - gradient_score) if has_gradient_issues else 100.0,
            (100.0 - compression_score) if has_compression else 100.0,
            text_consistency_score if is_text_consistent else (100.0 - text_consistency_score)
        ]
        
        overall_visual_score = float(np.mean(anomaly_scores))
        
        flags = []
        if not is_sharp:
            flags.append("BLURRY_IMAGE")
        if has_copy_paste:
            flags.append("COPY_PASTE_DETECTED")
        if has_pixel_anomalies:
            flags.append("PIXEL_ANOMALIES")
        if has_gradient_issues:
            flags.append("GRADIENT_INCONSISTENCY")
        if has_compression:
            flags.append("COMPRESSION_ARTIFACTS")
        if not is_text_consistent:
            flags.append("TEXT_INCONSISTENCY")
        
        status = "SUSPICIOUS" if len(flags) >= 2 or overall_visual_score < 50 else "CLEAR"
        
        analysis_report = {
            "image_hash": image_hash,
            "status": status,
            "overall_visual_score": round(overall_visual_score, 1),
            "blur_check": {
                "is_sharp": is_sharp,
                "variance": round(blur_variance, 2),
                "score": round(blur_score, 1)
            },
            "copy_paste_detection": {
                "detected": has_copy_paste,
                "score": round(copy_paste_score, 1)
            },
            "pixel_anomalies": {
                "detected": has_pixel_anomalies,
                "score": round(pixel_anomaly_score, 1)
            },
            "gradient_analysis": {
                "has_inconsistencies": has_gradient_issues,
                "score": round(gradient_score, 1)
            },
            "compression_artifacts": {
                "detected": has_compression,
                "score": round(compression_score, 1)
            },
            "text_consistency": {
                "consistent": is_text_consistent,
                "score": round(text_consistency_score, 1)
            },
            "flags": flags,
            "image_dimensions": [int(image.shape[1]), int(image.shape[0])],
            "image_channels": int(image.shape[2]) if len(image.shape) > 2 else 1
        }
        
        return analysis_report
