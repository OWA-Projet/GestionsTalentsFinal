// core/user.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface EntrepriseLight {
  id: number;
  nom: string;
}

export interface User {
  id: number;
  username: string;
  nom: string;
  prenom: string;
  poste: string;
  roles: string[];
  entreprise?: EntrepriseLight | null;
  is_staff?: boolean;
}

@Injectable({ providedIn: 'root' })
export class UserService {
  private API_URL = 'http://localhost:8000/api/utilisateurs/';
  private entrepriseURL = 'http://localhost:8000/api/entreprises/';
  private meUrl = 'http://localhost:8000/api/me/';
  constructor(private http: HttpClient) {}

  getAll(): Observable<User[]> {
    return this.http.get<User[]>(this.API_URL);
  }
  getOne(id: number | string): Observable<User> {
    return this.http.get<User>(`${this.API_URL}${id}/`);
  }
  create(data: any): Observable<any> {
    return this.http.post(this.API_URL, data);
  }
  update(id: number | string, data: any): Observable<any> {
    return this.http.put(`${this.API_URL}${id}/`, data);
  }
  delete(id: number | string): Observable<any> {
    return this.http.delete(`${this.API_URL}${id}/`);
  }
  getCurrentUser(): Observable<User | null> {
    return this.http.get<User>(this.meUrl);
  }
  /** Liste des entreprises pour la dropdown */
  getEntreprises(): Observable<EntrepriseLight[]> {
    return this.http.get<EntrepriseLight[]>(this.entrepriseURL);
  }
}
