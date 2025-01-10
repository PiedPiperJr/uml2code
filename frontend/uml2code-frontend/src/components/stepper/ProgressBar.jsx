import Spinner from "../icons/Spinner";

const ProgressBar = ({ progress, isUploading, progressMessage }) => {
  if (!isUploading && progress === 0) return null; // Do not show when not uploading and no progress

  return (
    <div className="space-y-2">
      {isUploading && progress < 100 && (
        <div className="flex items-center gap-2 text-gray-500">
          <Spinner />
          <span className="text-sm">{progressMessage}</span>
        </div>
      )}
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div 
          className="bg-blue-500 h-2 rounded-full transition-all duration-300"
          style={{ width: `${progress}%` }}
        />
      </div>
    </div>
  );
};

export default ProgressBar;
