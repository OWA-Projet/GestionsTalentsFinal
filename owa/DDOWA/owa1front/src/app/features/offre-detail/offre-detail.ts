import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { OffreEmploiService, OffreEmploi } from '../../core/offres.service';
import { CommonModule } from '@angular/common';
import { Observable, of } from 'rxjs';
import { switchMap, tap, catchError, map } from 'rxjs/operators';

@Component({
  selector: 'app-offre-detail',
  templateUrl: './offre-detail.html',
  styleUrls: ['./offre-detail.css'],
  standalone: true,
  imports: [CommonModule],
})
export class OffreDetailComponent {
  offre$: Observable<OffreEmploi | null>;
  isLoading = true;
  error: string | null = null;
  alertMsg: string | null = null;
  alertType: 'success' | 'error' = 'success';

  constructor(
    private route: ActivatedRoute,
    private offreService: OffreEmploiService,
    private router: Router
  ) {
    this.offre$ = this.route.paramMap.pipe(
      map(params => Number(params.get('id'))),
      tap(() => {
        this.isLoading = true;
        this.error = null;
      }),
      switchMap((id: number) => 
        this.offreService.getOneAcceuil(id).pipe(
          tap(() => this.isLoading = false),
          catchError(() => {
            this.error = 'Offre introuvable.';
            this.isLoading = false;
            return of(null);
          })
        )
      )
    );
  }

  onPostuler(id: number) {
    const userStr = localStorage.getItem('user');
    let user: any = null;
    try {
      user = userStr ? JSON.parse(userStr) : null;
    } catch {
      user = null;
    }

    const isCandidat = Array.isArray(user?.roles) && user.roles.includes('CANDIDAT');
    if (isCandidat) {
      this.router.navigate(['/postuler', id]);
    } else if(!user){
      this.alertMsg = "Vous devez être connecté  !";
       this.alertType = 'error';
    }
    else
    {
      this.alertMsg = "Vous n’avez pas accès à cette action !";
      this.alertType = 'error';
      setTimeout(() => this.alertMsg = null, 3500);
    }
  }
  getLogoUrl(imagePath: string | null | undefined): string {
  if (!imagePath) return 'assets/no-logo.png'; // Fallback si pas de logo
  return 'http://localhost:8000/' + imagePath.replace(/^\/+/, '');
}
}
