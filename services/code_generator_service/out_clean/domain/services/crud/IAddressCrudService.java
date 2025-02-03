// Service Interface Template
package mwm.domain.service.crud;

import mwm.domain.entities.Address;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import java.util.UUID;
import java.util.List;
import java.util.Optional;

public interface IAddressCrudService {
    Address create(Address entity);
    Address findById(UUID id);
    Page<Address> findAll(Pageable pageable);
    Address update(UUID id, Address entity);
    void delete(UUID id);
    
    
    
    
    
    
    
    
    
    
    
    
}