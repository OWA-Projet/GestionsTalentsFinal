import { Component } from '@angular/core';
import { MetierService, Metier } from '../../core/metier.service';
import { Router } from '@angular/router';
import { Observable, Subject, of } from 'rxjs';
import { switchMap, tap, catchError, shareReplay, startWith } from 'rxjs/operators';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-metier-list',
  templateUrl: './metier-list.component.html',
  styleUrls: ['./metier-list.component.css'],
  standalone: true,
  imports: [CommonModule]
})
export class MetierListComponent {
  private refresh$ = new Subject<void>();
  metiers$!: Observable<Metier[]>;
  error: string | null = null;

  constructor(
    private metierService: MetierService,
    private router: Router
  ) {}

  ngOnInit() {
    this.metiers$ = this.refresh$.pipe(
      startWith(void 0),
      switchMap(() =>
        this.metierService.getAll().pipe(
          tap(() => this.error = null),
          catchError(() => {
            this.error = "Erreur lors du chargement des métiers.";
            return of([] as Metier[]);
          })
        )
      ),
      shareReplay(1)
    );
  }

  ajouterMetier() {
    this.router.navigate(['/metier-formulaire']);
  }

  modifierMetier(id: number) {
    this.router.navigate(['/metier-formulaire', id]);
  }

  supprimerMetier(id: number) {
    if (!confirm("Supprimer ce métier ?")) return;
    this.metierService.delete(id).subscribe({
      next: () => this.refresh$.next(),
      error: () => this.error = "Erreur lors de la suppression."
    });
  }
}
