import { Component } from '@angular/core';
import { OffreEmploi, OffreEmploiService } from '../../core/offres.service';
import { Router } from '@angular/router';
import { Observable, Subject, of } from 'rxjs';
import { switchMap, tap, catchError, shareReplay, startWith } from 'rxjs/operators';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-offres-rh',
  templateUrl: './offres-rh.component.html',
  styleUrls: ['./offres-rh.component.css'],
  standalone: true,
  imports: [CommonModule]
})
export class OffresRhComponent {
  private refresh$ = new Subject<void>();
  offres$!: Observable<OffreEmploi[]>;
  error: string | null = null;
  user: any = null;

  constructor(
    private offreService: OffreEmploiService,
    private router: Router
  ) {}

  ngOnInit() {
    const userStr = localStorage.getItem('user');
    try {
      this.user = userStr ? JSON.parse(userStr) : null;
    } catch {
      this.user = null;
    }

    this.offres$ = this.refresh$.pipe(
  startWith(void 0),
  switchMap(() =>
    this.offreService.getAll(this.user.entreprise.id).pipe(
      tap(() => this.error = null),
      catchError(err => {
        this.error = "Erreur lors du chargement des offres.";
        return of([] as OffreEmploi[]);
      })
    )
  ),
  shareReplay(1)
);
  }

  ajouterOffre(identreprise: number) {
    this.router.navigate(['/offres-formulaire/entreprise', identreprise]);
  }

  modifierOffre(id: number) {
    this.router.navigate(['/offres-formulaire', id]);
  }

  supprimerOffre(id: number) {
    if (!confirm("Supprimer cette offre ?")) return;
    this.offreService.delete(id).subscribe({
      next: () => this.refresh$.next(), // Déclenche le refresh
      error: () => this.error = "Erreur lors de la suppression."
    });
  }
  voirCVs(id: number) {
    this.router.navigate(['/offres-cv', id, 'cvs']);
  }
  
}
