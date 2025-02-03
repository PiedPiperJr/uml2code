package mwm.infrastructure.repositories;

import mwm.domain.entities.Professor;
import mwm.domain.repositories.IProfessorRepository;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.UUID;
import java.util.List;

@Repository
public interface ProfessorJpaRepository extends JpaRepository<Professor, UUID>, 
    IProfessorRepository<Professor, UUID> {
    
    
    
    
    
    
    
    
    
    
    
    
    @Query("SELECT e FROM Professor e LEFT JOIN FETCH e.adressess WHERE e.id = :id")
    Optional<Professor> findByIdWithAdressess(@Param("id") UUID id);
    
    
    
}