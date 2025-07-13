/**
 * Componente de ejemplo con mejores prácticas
 */

import React, { memo, useMemo, useCallback } from 'react';

interface ButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  variant?: 'primary' | 'secondary' | 'danger';
  disabled?: boolean;
  loading?: boolean;
  className?: string;
}

const Button = memo<ButtonProps>(({ 
  children, 
  onClick, 
  variant = 'primary', 
  disabled = false, 
  loading = false,
  className = ''
}) => {
  const baseStyles = 'px-4 py-2 rounded-md font-medium focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors';
  
  const variantStyles = useMemo(() => {
    switch (variant) {
      case 'primary':
        return 'bg-blue-600 hover:bg-blue-700 text-white focus:ring-blue-500';
      case 'secondary':
        return 'bg-gray-200 hover:bg-gray-300 text-gray-900 focus:ring-gray-500';
      case 'danger':
        return 'bg-red-600 hover:bg-red-700 text-white focus:ring-red-500';
      default:
        return 'bg-blue-600 hover:bg-blue-700 text-white focus:ring-blue-500';
    }
  }, [variant]);

  const handleClick = useCallback(() => {
    if (!disabled && !loading && onClick) {
      onClick();
    }
  }, [disabled, loading, onClick]);

  const combinedClassName = `${baseStyles} ${variantStyles} ${
    disabled || loading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'
  } ${className}`.trim();

  return (
    <button
      type="button"
      className={combinedClassName}
      onClick={handleClick}
      disabled={disabled || loading}
      aria-disabled={disabled || loading}
    >
      {loading ? (
        <span className="flex items-center">
          <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Cargando...
        </span>
      ) : (
        children
      )}
    </button>
  );
});

Button.displayName = 'Button';

export default Button;