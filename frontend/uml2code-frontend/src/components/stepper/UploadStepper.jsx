import { useState, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import { FaCloudUploadAlt, FaTrash, FaDownload } from 'react-icons/fa';
import Stepper from './Stepper';
import ProgressBar from './ProgressBar';
import LayoutToggle from './LayoutToggle';

const UploadStepper = () => {
  const [layout, setLayout] = useState('horizontal');
  const [currentStep, setCurrentStep] = useState(1);
  const [fileProgresses, setFileProgresses] = useState({});
  const [processingProgresses, setProcessingProgresses] = useState({});
  const [files, setFiles] = useState([]);
  const [downloadLinks, setDownloadLinks] = useState([]);
  const [currentFileIndex, setCurrentFileIndex] = useState(0);

  const steps = [
    { label: 'Prepare Files', icon: '1', content: 'Upload and prepare your .drawio files for processing.' },
    { label: 'Uploading', icon: '2', content: 'Files are being uploaded to the server. Please wait.' },
    { label: 'Processing', icon: '3', content: 'Your files are being processed. This may take some time.' },
    { label: 'Download', icon: '4', content: 'Upload complete! Download your generated code files.' }
  ];

  const onDrop = (acceptedFiles) => {
    const validFiles = acceptedFiles.filter(file => file.name.endsWith('.drawio'));
    if (validFiles.length > 0) {
      const updatedFiles = validFiles.map(file => ({
        file,
        name: file.name,
      }));
      setFiles(prev => [...prev, ...updatedFiles]);
      setDownloadLinks([]);
    } else {
      alert('Please upload .drawio files.');
    }
  };

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: '.drawio',
    multiple: true
  });

  const removeFile = (index) => {
    const newFiles = files.filter((_, i) => i !== index);
    setFiles(newFiles);
  };

  const uploadFiles = async () => {
    if (files.length === 0) {
      alert('Please upload at least one .drawio file.');
      return;
    }
  
    setCurrentStep(2);
    const newDownloadLinks = [];
    const newFileProgresses = {};
    const newProcessingProgresses = {};
  
    for (let i = 0; i < files.length; i++) {
      const file = files[i].file;
      setCurrentFileIndex(i);
  
      try {
        // Upload progress tracking
        const uploadProgress = (event) => {
          const percentComplete = Math.round((event.loaded / event.total) * 100);
          newFileProgresses[file.name] = percentComplete;
          setFileProgresses({...newFileProgresses});
        };
  
        const formData = new FormData();
        formData.append('file', file);
  
        const response = await fetch('http://127.0.0.1:5000/process', {
          method: 'POST',
          body: formData,
          xhr: (xhr) => {
            xhr.upload.addEventListener('progress', uploadProgress);
          }
        });
  
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Upload failed');
        }
  
        // Move to Processing step
        setCurrentStep(3);
  
        // Simulate processing with incremental progress
        for (let progress = 0; progress <= 100; progress += 20) {
          newProcessingProgresses[file.name] = progress;
          setProcessingProgresses({...newProcessingProgresses});
          await new Promise(resolve => setTimeout(resolve, 300));
        }
  
        // Get the blob for download
        const blob = await response.blob();
        const downloadUrl = URL.createObjectURL(blob);
        newDownloadLinks.push(downloadUrl);
  
      } catch (error) {
        console.error(`Error processing ${file.name}:`, error);
        alert(`Error processing ${file.name}: ${error.message}`);
        handleReset();
        return;
      }
    }
  
    setDownloadLinks(newDownloadLinks);
    setCurrentStep(4);
  };

  const handleReset = () => {
    setCurrentStep(1);
    setFiles([]);
    setFileProgresses({});
    setProcessingProgresses({});
    setDownloadLinks([]);
    setCurrentFileIndex(0);
  };

  return (
    <div className="space-y-8 p-4">
      <LayoutToggle 
        layout={layout}
        onToggle={() => setLayout(prev => (prev === 'horizontal' ? 'vertical' : 'horizontal'))}
      />

      <div className="w-full max-w-3xl mx-auto bg-white rounded-lg shadow-md p-6">
        <div className={`flex ${layout === 'vertical' ? 'flex-row gap-12' : 'flex-col gap-8'}`}>
          <div className="flex flex-col w-full">
            <h3 className="text-xl font-semibold">{steps[currentStep - 1].label}</h3>
            <p className="text-sm text-gray-600 mt-2">{steps[currentStep - 1].content}</p>

            {currentStep === 1 && (
              <div className="mt-2">
                {!files.length && 
                  <div
                    {...getRootProps()}
                    className="border-2 border-dashed border-gray-300 p-6 rounded-md text-center cursor-pointer">
                    <input {...getInputProps()} />
                    <FaCloudUploadAlt className="text-8xl text-gray-500 mb-4 mx-auto" />
                    <p className="text-lg">Drag & Drop .drawio files here, or click to select</p>
                  </div>
                }

                {files.length > 0 && (
                  <div className="mt-4 space-y-2">
                    {files.map((file, index) => (
                      <div key={index} className="flex justify-between items-center bg-gray-100 p-2 rounded">
                        <span>{file.name}</span>
                        <button 
                          onClick={() => removeFile(index)} 
                          className="text-red-500 hover:text-red-700"
                        >
                          <FaTrash />
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {currentStep === 2 && (
              <div className="space-y-2">
                {files.map((file, index) => (
                  <div key={index} className="flex items-center space-x-2">
                    <div className="flex-grow">
                      <div className="flex justify-between items-center mb-1">
                        <p className="text-sm font-medium">{file.name}</p>
                        <span className="text-xs">{fileProgresses[file.name] || 0}%</span>
                      </div>
                      <ProgressBar 
                        progress={fileProgresses[file.name] || 0} 
                        isUploading={true} 
                        progressMessage=""
                      />
                    </div>
                  </div>
                ))}
              </div>
            )}

            {currentStep === 3 && (
              <div className="space-y-2">
                {files.map((file, index) => (
                  <div key={index} className="flex items-center space-x-2">
                    <div className="flex-grow">
                      <div className="flex justify-between items-center mb-1">
                        <p className="text-sm font-medium">{file.name}</p>
                        <span className="text-xs">{processingProgresses[file.name] || 0}%</span>
                      </div>
                      <ProgressBar 
                        progress={processingProgresses[file.name] || 0} 
                        isUploading={false} 
                        progressMessage="Processing"
                      />
                    </div>
                  </div>
                ))}
              </div>
            )}

            {currentStep === 4 && (
              <div className="space-y-2">
                {files.map((file, index) => (
                  <div 
                    key={index} 
                    className="flex items-center justify-between bg-gray-100 p-2 rounded"
                  >
                    <span className="truncate pr-2">{file.name.replace('.drawio', '')}</span>
                    <a 
                      href={downloadLinks[index]} 
                      download={`generated_classes_${file.name.replace('.drawio', '.zip')}`}
                      className="flex items-center bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600 no-underline"
                    >
                      <FaDownload className="mr-2" /> Download
                    </a>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="flex flex-col gap-4 w-full">
            <Stepper
              steps={steps}
              currentStep={currentStep}
              layout={layout}
            />

            <div className="flex justify-center items-center gap-4">
              {currentStep === 1 && (
                <button
                  onClick={uploadFiles}
                  disabled={files.length === 0}
                  className={`px-4 py-2 rounded-md bg-blue-500 text-white ${
                    files.length === 0
                      ? 'opacity-50 cursor-not-allowed'
                      : 'hover:bg-blue-600'
                  } transition-colors duration-200`}
                >
                  Start Upload
                </button>
              )}

              {(currentStep === 2 || currentStep === 3 || currentStep === 4) && (
                <button
                  onClick={handleReset}
                  className="px-4 py-2 rounded-md bg-white text-gray-700 border border-gray-300 hover:bg-gray-50"
                >
                  Reset
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UploadStepper;