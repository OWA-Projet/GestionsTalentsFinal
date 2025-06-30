import { Component } from '@angular/core';
import { OffreEmploiService, OffreEmploi } from '../../core/offres.service';
import { Router, NavigationEnd } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../core/auth.service';
import { Observable, BehaviorSubject, combineLatest, merge } from 'rxjs';
import { filter, startWith, switchMap, catchError, map, tap } from 'rxjs/operators';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-acceuil',
  templateUrl: './acceuil.component.html',
  styleUrls: ['./acceuil.component.css'],
  standalone: true,
  imports: [CommonModule, FormsModule],
})
export class AcceuilComponent {
  // Barre de recherche
  searchTerm$ = new BehaviorSubject<string>('');
  offresList: OffreEmploi[] = [];
  offresList$ = new BehaviorSubject<OffreEmploi[]>([]);
  isLoading = true;
  error: string | null = null;

  filteredOffres$: Observable<OffreEmploi[]>;

  constructor(
    private offreService: OffreEmploiService,
    private router: Router,
    private authservice: AuthService
  ) {
    // Actualisation à chaque navigation et chargement initial
    merge(
      this.router.events.pipe(
        filter(event => event instanceof NavigationEnd),
        filter(() => this.router.url === '/' || this.router.url.startsWith('/acceuil'))
      ),
      [null]
    ).pipe(
      startWith(null),
      switchMap(() => {
        this.isLoading = true;
        this.error = null;
        return this.offreService.getAllAcceuil().pipe(
          tap(data => {
            this.isLoading = false;
            this.offresList = data;
            this.offresList$.next(data);
          }),
          catchError(err => {
            this.error = "Erreur lors du chargement des offres.";
            this.isLoading = false;
            this.offresList = [];
            this.offresList$.next([]);
            return [[]];
          })
        );
      })
    ).subscribe();

    // Observable filtré réactif
    this.filteredOffres$ = combineLatest([
      this.offresList$,
      this.searchTerm$
    ]).pipe(
      map(([offres, term]) => {
        term = term.trim().toLowerCase();
        if (!term) return offres;
        return offres.filter(offre =>
          (offre.libelle || '').toLowerCase().includes(term) ||
          (offre.entreprise?.nom || '').toLowerCase().includes(term) ||
          (offre.metier_propose || '').toLowerCase().includes(term) ||
          (offre.type_contrat || '').toLowerCase().includes(term)
        );
      })
    );
  }

  onSearchChange(term: string) {
    this.searchTerm$.next(term);
  }

  voirDetail(id: number) {
    this.router.navigate(['/detail-offre', id]);
  }

  getLogoUrl(imagePath: string | null | undefined): string {
    if (!imagePath) return 'assets/no-logo.png'; // logo fallback local
    return 'http://localhost:8000/' + imagePath.replace(/^\/+/, '');
  }

  // ----- GESTION ROLES & MENU -----

  get currentUser(): any {
    const userStr = localStorage.getItem('user');
    try {
      return userStr ? JSON.parse(userStr) : null;
    } catch {
      return null;
    }
  }

  isRH(): boolean {
    return Array.isArray(this.currentUser?.roles) && this.currentUser.roles.includes('RH');
  }
  isCANDIDAT(): boolean {
    return Array.isArray(this.currentUser?.roles) && this.currentUser.roles.includes('CANDIDAT');
  }
  ISADMIN(): boolean {
    return Array.isArray(this.currentUser?.roles) && this.currentUser.roles.includes('ADMIN');
  }
  ISCONNECTED(): boolean {
    const userStr = localStorage.getItem('user');
    let user: any = null;
    try {
      user = userStr ? JSON.parse(userStr) : null;
    } catch {
      user = null;
    }
    return !!user;
  }

  ISVISITEUR(): boolean {
    return !this.currentUser;
  }
  isAuthenticated(): boolean {
    return !this.ISVISITEUR();
  }
  tocontact() { this.router.navigate(['/contact']) }
  toabout() { this.router.navigate(['/about']) }
  toregister() { this.router.navigate(['/register']); }
  tologin() { this.router.navigate(['/login']); }
  touser() { this.router.navigate(['/user-list']); }
  tometier() { this.router.navigate(['/metier-list']); }
  toentreprise() { this.router.navigate(['/entreprise']); }
  toespace() { this.router.navigate(['/espace-candidat']); }
  toprofile() { this.router.navigate(['/profile']); }
  torhoffer() {
    const currentuser = this.currentUser;
    if (currentuser?.entreprise === null) {
      window.alert("🚫 Aucune entreprise associée à votre compte , veuillez communiquer votre entreprise !");
    } else {
      this.router.navigate(['/offres-rh']);
    }
  }
  disconnect() {
    this.authservice.logout().subscribe({
      next: _ => {
        this.router.navigate(['/login']);
      }
    });
  }
}
