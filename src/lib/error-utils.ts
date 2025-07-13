/**
 * Utilidades para manejo de errores y logging
 */

type ErrorWithOptionalStack = ErrorConstructor & {
  captureStackTrace?: (targetObject: object, constructorOpt?: Function | undefined) => void;
};

export class AppError extends Error {
  constructor(
    message: string,
    public statusCode: number = 500,
    public isOperational: boolean = true
  ) {
    super(message);
    const ErrorWithStackTrace = Error as ErrorWithOptionalStack;
    if (ErrorWithStackTrace.captureStackTrace) {
      ErrorWithStackTrace.captureStackTrace(this, this.constructor);
    }
  }
}

export const handleAsync = <T extends any[], R>(
  fn: (...args: T) => Promise<R>
) => {
  return (...args: T): Promise<R> => {
    return fn(...args).catch((error) => {
      console.error('Error in async function:', error);
      throw error;
    });
  };
};

export const safeJsonParse = <T>(
  json: string,
  fallback: T
): T => {
  try {
    return JSON.parse(json);
  } catch {
    return fallback;
  }
};

export const logger = {
  info: (message: string, data?: any) => {
    if (typeof window === 'undefined') {
      console.log(`[INFO] ${message}`, data || '');
    }
  },
  error: (message: string, error?: any) => {
    console.error(`[ERROR] ${message}`, error || '');
  },
  warn: (message: string, data?: any) => {
    console.warn(`[WARN] ${message}`, data || '');
  }
};