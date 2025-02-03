package mwm.infrastructure.repositories;

import mwm.domain.entities.Person;
import mwm.domain.repositories.IPersonRepository;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.UUID;
import java.util.List;

@Repository
public interface PersonJpaRepository extends JpaRepository<Person, UUID>, 
    IPersonRepository<Person, UUID> {
    
    
    
    
    
    
    
    
    
    
    
    
    
    
}