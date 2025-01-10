import StepperDot from "./StepperDot"

const Stepper = ({ steps, currentStep, layout }) => (
    <div className={`
      relative flex 
      ${layout === 'vertical' ? 'flex-col' : 'flex-row justify-between w-full'}
    `}>
      {/* Connection lines */}
      {layout === 'horizontal' && (
        <div className="absolute top-5 left-0 w-full h-0.5 bg-gray-200">
          <div 
            className="h-full bg-blue-500 transition-all duration-300"
            style={{ 
              width: `${((currentStep - 1) / (steps.length - 1)) * 100}%`
            }}
          />
        </div>
      )}
  
      {steps.map((step, index) => {
        const isActive = index + 1 === currentStep;
        const isCompleted = index + 1 < currentStep;
  
        return (
          <div
            key={index}
            className={`
              relative flex 
              ${layout === 'vertical' ? 'flex-row items-center' : 'flex-col items-center'}
              ${layout === 'vertical' ? 'mb-8 last:mb-0' : ''}
              z-10
            `}
          >
            {/* Vertical connection line */}
            {layout === 'vertical' && index < steps.length - 1 && (
              <div className="absolute left-5 top-10 w-0.5 h-16 -z-10">
                <div className="w-full h-full bg-gray-200">
                  <div 
                    className="w-full bg-blue-500 transition-all duration-300"
                    style={{ 
                      height: isCompleted ? '100%' : '0%'
                    }}
                  />
                </div>
              </div>
            )}
  
            <StepperDot 
              step={step}
              isActive={isActive}
              isCompleted={isCompleted}
            />
            
            {/* Step label */}
            <div className={`
              ${layout === 'vertical' ? 'ml-4' : 'mt-2'}
              min-w-[80px] text-center
            `}>
              <span className={`
                text-sm font-medium
                ${isActive ? 'text-blue-500' : isCompleted ? 'text-blue-500' : 'text-gray-500'}
              `}>
                {step.label}
              </span>
            </div>
          </div>
        );
      })}
    </div>
  );
  
  export default Stepper;