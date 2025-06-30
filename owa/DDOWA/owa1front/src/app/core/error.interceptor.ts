// error.interceptor.ts
import { HttpInterceptorFn } from '@angular/common/http';
import { catchError } from 'rxjs/operators';

export const ErrorInterceptor: HttpInterceptorFn = (req, next) => {
  return next(req).pipe(
    catchError((error) => {
      let msg = "Erreur inconnue.";
      if (error.error?.detail) msg = error.error.detail;
      alert(msg); // ou ton toast, etc.
      throw error;
    })
  );
};

