import { AppError, logger } from './error-utils';

export type ApiResponse<T = any> = {
  data?: T;
  error?: string;
  statusCode: number;
};

export function createApiResponse<T>(
  data?: T,
  error?: string,
  statusCode: number = 200
): ApiResponse<T> {
  return {
    ...(data && { data }),
    ...(error && { error }),
    statusCode
  };
}

export async function handleApiError(error: unknown): Promise<ApiResponse> {
  logger.error('API Error:', error);

  if (error instanceof AppError) {
    return createApiResponse(undefined, error.message, error.statusCode);
  }

  if (error instanceof Error) {
    return createApiResponse(undefined, error.message, 500);
  }

  return createApiResponse(undefined, 'Internal Server Error', 500);
}

export function validateRequest<T>(
  data: any,
  validator: (data: any) => data is T
): T {
  if (!validator(data)) {
    throw new AppError('Invalid request data', 400, undefined);
  }
  return data;
}