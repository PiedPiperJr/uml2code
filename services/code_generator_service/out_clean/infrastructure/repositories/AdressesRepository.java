package mwm.infrastructure.repositories;

import mwm.domain.entities.Adresses;
import mwm.domain.repositories.IAdressesRepository;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.UUID;
import java.util.List;

@Repository
public interface AdressesJpaRepository extends JpaRepository<Adresses, UUID>, 
    IAdressesRepository<Adresses, UUID> {
    
    
    
    
    
    
    
    
    
    
    
    
    
    
}