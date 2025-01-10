import CheckMark from "../icons/Checkmark"

const StepperDot = ({ step, isActive, isCompleted }) => (
    <div
      className={`
        flex h-10 w-10 shrink-0 items-center justify-center rounded-full
        transition-colors duration-300 ease-in-out
        ${isCompleted ? 'bg-blue-500' : isActive ? 'border-2 border-blue-500 bg-white' : 'border-2 border-gray-200 bg-white'}
      `}
    >
      {isCompleted ? (
        <CheckMark />
      ) : (
        <span className={`text-sm font-medium ${isActive ? 'text-blue-500' : 'text-gray-500'}`}>
          {step.icon}
        </span>
      )}
    </div>
  );
  
  export default StepperDot;