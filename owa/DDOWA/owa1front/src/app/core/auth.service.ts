import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, tap } from 'rxjs';

// Helper universel :
function isBrowser(): boolean {
  return typeof window !== 'undefined' && typeof localStorage !== 'undefined';
}

export interface RegisterPayload {
  username: string;
  password: string;
  nom: string;
  prenom: string;
  poste: string;
  roles?: string[]; // optionnel
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  private api = 'http://127.0.0.1:8000/api'; // Adapter si besoin
  user$ = new BehaviorSubject<any>(null);

  constructor(private http: HttpClient) {
    if (isBrowser()) {
      const user = localStorage.getItem('user');
      if (user) this.user$.next(JSON.parse(user));
    }
  }

  login(data: { username: string, password: string }) {
    return this.http.post<any>(`${this.api}/login/`, data).pipe(
      tap(res => {
        if (isBrowser()) {
          localStorage.setItem('access', res.access);
          localStorage.setItem('refresh', res.refresh);
          localStorage.setItem('user', JSON.stringify(res.user));
        }
        this.user$.next(res.user);
      })
    );
  }

  logout() {
    return this.http.post(`${this.api}/logout/`, {}).pipe(
      tap(_ => {
        if (isBrowser()) localStorage.clear();
        this.user$.next(null);
      })
    );
  }

  register(payload: RegisterPayload): Observable<any> {
    return this.http.post<any>('http://127.0.0.1:8000/api/register/', payload);
  }

  get token() {
    return isBrowser() ? localStorage.getItem('access') : null;
  }
  get user() {
    return this.user$.value;
  }
  get roles(): string[] {
    return this.user?.roles || [];
  }
  isRH() {
    return this.roles.includes('RH');
  }
  isCandidat() {
    return this.roles.includes('CANDIDAT');
  }
  isAdmin() {
    return this.roles.includes('ADMIN');
  }
  isLoggedIn() {
    return !!this.token;
  }
}
