// src/app/core/entreprise.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Entreprise {
  id: number;
  nom: string;
  adresse_siege: string;
  image?: string | null;
  entreprise_infos?: string;
}

@Injectable({ providedIn: 'root' })
export class EntrepriseService {
  private apiUrl = 'http://localhost:8000/api/entreprises/';

  constructor(private http: HttpClient) {}

  getAll(): Observable<Entreprise[]> {
    return this.http.get<Entreprise[]>(this.apiUrl);
  }
  getOne(id: number): Observable<Entreprise> {
    return this.http.get<Entreprise>(`${this.apiUrl}${id}/`);
  }
  create(ent: Entreprise, file?: File): Observable<Entreprise> {
    const formData = new FormData();
    Object.entries(ent).forEach(([key, value]) => {
      if (value !== undefined && value !== null) formData.append(key, value as any);
    });
    if (file) formData.append('image', file, file.name);
    return this.http.post<Entreprise>(this.apiUrl, formData);
  }
  update(id: number, ent: Entreprise, file?: File): Observable<Entreprise> {
    const formData = new FormData();
    Object.entries(ent).forEach(([key, value]) => {
      if (value !== undefined && value !== null) formData.append(key, value as any);
    });
    if (file) formData.append('image', file, file.name);
    return this.http.put<Entreprise>(`${this.apiUrl}${id}/`, formData);
  }
  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}${id}/`);
  }
}
