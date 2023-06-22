import React, {useState, useRef} from "react";
import axios from "axios"
import './App.css'; 
import logo from "./resources/logo.png";
import downloadimg from "./resources/download1.png"
import loader from "./resources/loader.gif"
import uploadimg from "./resources/upload1.png"
import {useDropzone} from 'react-dropzone';

function App() {
  const [Name,setName]=useState()
  const [state,setState]= useState(2)
  const [url,seturl] = useState()
  const fileInputRef = useRef();

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: "video/mp4, video/mov, video/avi",
    onDrop: (acceptedFiles) => {
      const files = acceptedFiles;
      setState(-1);
      let upvideo = new FormData();
      upvideo.append('file', files[0]);
      const filename = String(files[0].name);
      const fileUrl = URL.createObjectURL(files[0]); // Get the URL of the file
      seturl(fileUrl);
      setName(filename);
      axios.post("http://localhost:5000/upload", upvideo).then(
        res => {
          console.log(res);
          setState(1);
        }
      );
    }
  });

  const Detectvideo = () =>{
    setState(-1)
    let detector = new FormData();
    detector.append('filename',Name)
    axios.post("http://localhost:5000/convert",{filename : Name, model : "yolov8n"}).then(
      res => {
        console.log(res)
        setState(2)
      }
    )
  }

  const Downloadfile = () =>{
    setState(-1)
    axios({
      url: 'http://localhost:5000/downloadfile',
      method: 'GET',
      responseType: 'blob',
    }).then((response) => {
      const href = URL.createObjectURL(response.data);
      const link = document.createElement('a');
      link.href = href;
      link.setAttribute('download', 'video');
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(href);
      setState(2)
  });
  }

  return (
    <div className="App">
       <div className="headingdiv">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="headingtxt">Vehicle Detection</h1>
        </div>
        {(state === -1)?(
        <div>
          <img src={loader} alt="loader" className="Loader"/>
          <h3 className="Loadingtxt">Loading</h3>
        </div>):(<div></div>)}
        {(state === 0)?(
        <div className="upbox-cont">
          <div {...getRootProps()} className="dragbox">
            <input
              {...getInputProps()}
              type="file"
              accept="video/*"
              className="imginput"
              ref={fileInputRef}
            />
            <img src={uploadimg} className="upimg" alt = "up" draggable="false" />
            <h1 className="droptxt">{
              isDragActive? ("Drop the File Here") : ("Drop the File or Click Here to Upload")}
            </h1>
          </div>
        </div>):(
          <div></div>
        )}

        {(state === 1)?(<div>
          <div className="hzbar">
            <div className="imgcont" style={{ position: "relative" }}>
              <div className="canvas-container">
                <video
                  muted
                  playsInline
                  controls
                >
                  {url && <source src={url} type="video/mp4" />}
                </video>
              </div>
            </div>
            <div className="setbar">
              <h2 className="titleset">Settings</h2>
              <hr></hr>
              <div className="sectionp2">
            
                <h5 className="lstset1">Model</h5>
                <h5 className="lstset2">YOLOv8n</h5>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="lstset3 bi bi-chevron-right" viewBox="0 0 16 16">
                <path fill-rule="evenodd" d="M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708z"/>
              </svg>
              
                </div>
              <div className="btnbox">
                <button type="button" className='detectbtn' onClick={Detectvideo}>Detect</button>
              </div>
            </div>
          </div>
        </div>):(<div></div>)}
        {(state === 2)?(
        <div className="downbox-cont">
          <img src={downloadimg} className="downimg" alt="down" draggable="false" />
          <a className = "downtxt" onClick={Downloadfile}>Click here to download output</a>
        </div>
        ):(<div></div>)}    


    </div>
  );
}

export default App;
