
export interface Entreprise {
  id: number;
  nom: string;
  adresse_siege: string;
  image?: string | null;
  entreprise_infos?: string;
}


export interface OffreEmploi {
  id: number;
  libelle: string;
  description?: string;
  metier_propose: string;
  secteur_activite: string;
  Experience_requise: string;
  niveau_etude: string;
  type_contrat: string;
  date_publication: string;
  date_expiration: string;
  profil_recherche?: string;
  image?: string | null;
  entreprise?: Entreprise | null;         // Récupération
  entreprise_id?: number | null;          // Création/édition
}



// src/app/core/services/offre-emploi.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class OffreEmploiService {
  private apiUrl = "http://localhost:8000/api/offres-emploi/";
  private apiUrlAcceuil = "http://localhost:8000/api/offres-acceuil/";

  constructor(private http: HttpClient) {}

  // Liste toutes les offres (GET /offres-emploi/)
  getAll(idEntreprise: number): Observable<OffreEmploi[]> {
  const params = new HttpParams().set('entreprise', idEntreprise.toString());
  return this.http.get<OffreEmploi[]>(this.apiUrl, { params });
}

   
  getAllAcceuil(): Observable<OffreEmploi[]> {
    return this.http.get<OffreEmploi[]>(this.apiUrlAcceuil);
  }
  
   // Récupère une offre par id (GET /offres-emploi/{id}/)
  getOneAcceuil(id: number): Observable<OffreEmploi> {
    return this.http.get<OffreEmploi>(`${this.apiUrlAcceuil}${id}/`);
  }

  // Récupère une offre par id (GET /offres-emploi/{id}/)
  getOne(id: number): Observable<OffreEmploi> {
    return this.http.get<OffreEmploi>(`${this.apiUrl}${id}/`);
  }

  create(offre: OffreEmploi, file?: File): Observable<OffreEmploi> {
  const formData = new FormData();
  Object.entries(offre).forEach(([key, value]) => {
    // N'ajoute que entreprise_id (PAS l'objet entreprise)
    if (key === 'entreprise' || key === 'entreprise_infos') return;
    if (key === 'entreprise_id' && value !== undefined && value !== null) {
      formData.append('entreprise_id', value.toString());
    } else if (value !== undefined && value !== null) {
      formData.append(key, value as any);
    }
  });
  if (file) {
    formData.append('image', file, file.name);
  }
  return this.http.post<OffreEmploi>(this.apiUrl, formData);
}



  // Modifie entièrement une offre (PUT /offres-emploi/{id}/)
  update(id: number, offre: OffreEmploi, file?: File): Observable<OffreEmploi> {
  const formData = new FormData();
  Object.entries(offre).forEach(([key, value]) => {
    if (key === 'entreprise' || key === 'entreprise_infos') return;
    if (key === 'entreprise_id' && value !== undefined && value !== null) {
      formData.append('entreprise_id', value.toString());
    } else if (value !== undefined && value !== null) {
      formData.append(key, value as any);
    }
  });
  if (file) {
    formData.append('image', file, file.name);
  }
  return this.http.put<OffreEmploi>(`${this.apiUrl}${id}/`, formData);
}


  // Modifie partiellement une offre (PATCH /offres-emploi/{id}/)
  partialUpdate(id: number, partial: Partial<OffreEmploi>): Observable<OffreEmploi> {
    return this.http.patch<OffreEmploi>(`${this.apiUrl}${id}/`, partial);
  }

  // Supprime une offre (DELETE /offres-emploi/{id}/)
  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}${id}/`);
  }
}
