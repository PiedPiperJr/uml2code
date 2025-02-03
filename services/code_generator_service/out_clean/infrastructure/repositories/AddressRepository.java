package mwm.infrastructure.repositories;

import mwm.domain.entities.Address;
import mwm.domain.repositories.IAddressRepository;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.UUID;
import java.util.List;

@Repository
public interface AddressJpaRepository extends JpaRepository<Address, UUID>, 
    IAddressRepository<Address, UUID> {
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
}