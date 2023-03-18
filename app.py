# using video_transformer_factory

import cv2
import numpy as np
from PIL import Image
import av
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration, VideoTransformerBase
import threading
from typing import Union
import torch
from PIL import Image


RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

def main():
    if st.button("yolov5s"):
        st.model = torch.hub.load('ultralytics/yolov5', 'yolov5s',  _verbose=False)

    if st.button("custom_model"):
        st.model = torch.hub.load('./yolov5/', 'custom', path='my_face_detection_model.pt', source='local')


    class VideoTransformer(VideoTransformerBase):
        frame_lock: threading.Lock  # `transform()` is running in another thread, then a lock object is used here for thread-safety.
        in_image: Union[np.ndarray, None]
        out_image: Union[np.ndarray, None]

        def __init__(self) -> None:
            self.frame_lock = threading.Lock()
            self.in_image = None
            self.out_image = None

        def transform(self, frame: av.VideoFrame) -> np.ndarray:
            in_image = frame.to_ndarray(format="bgr24")

            out_image = in_image[:, ::-1, :]  # Simple flipping for example.

            im_pil = Image.fromarray(out_image)
            results = st.model(im_pil)
            bbox_img = np.array(results.render()[0])

            #return av.VideoFrame.from_ndarray(bbox_img, format="bgr24")
            return bbox_img
        
    webrtc_ctx = webrtc_streamer(
        key="WYH",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIGURATION,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
        video_transformer_factory=VideoTransformer
    )

if __name__ == "__main__":
    main()