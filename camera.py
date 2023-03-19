import cv2
import numpy as np
from PIL import Image
import av
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)


class VideoProcessor:
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        # img = process(img)

         # vision processing
        flipped = img[:, ::-1, :]

        # model processing
        im_pil = Image.fromarray(flipped)
        #results = st.model(im_pil)
        #bbox_img = np.array(results.render()[0])

        return av.VideoFrame.from_ndarray(img, format="bgr24")
    
webrtc_ctx = webrtc_streamer(
    key="WYH",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints={"video": True, "audio": False},
    video_processor_factory=VideoProcessor,
    async_processing=True,
)


