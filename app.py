# using  video_processor_factory
import numpy as np
from PIL import Image
import av
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration, VideoProcessorBase
import torch

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

#st.model = torch.hub.load('./yolov5/', 'custom', path='my_face_detection_model.pt', source='local')
if st.button("yolov5s"):
    st.model = torch.hub.load('ultralytics/yolov5', 'yolov5s',  _verbose=False)

if st.button("custom_model"):
    #st.model = torch.hub.load('yolov5/', 'custom', path='my_face_detection_model.pt', source='local')
    st.model  = torch.hub.load('ultralytics/yolov5', 'custom', path='my_face_detection_model.pt', force_reload=True) 


class VideoProcessor(VideoProcessorBase):
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        # img = process(img)

         # vision processing
        flipped = img[:, ::-1, :]

        # model processing
        im_pil = Image.fromarray(flipped)
        results = st.model(im_pil)
        bbox_img = np.array(results.render()[0])

        return av.VideoFrame.from_ndarray(bbox_img, format="bgr24")
    
webrtc_ctx = webrtc_streamer(
    key="WYH",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints={"video": True, "audio": False},
    video_processor_factory=VideoProcessor,
    async_processing=True,
)