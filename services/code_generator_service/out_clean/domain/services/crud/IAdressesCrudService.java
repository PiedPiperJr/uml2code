// Service Interface Template
package mwm.domain.service.crud;

import mwm.domain.entities.Adresses;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import java.util.UUID;
import java.util.List;
import java.util.Optional;

public interface IAdressesCrudService {
    Adresses create(Adresses entity);
    Adresses findById(UUID id);
    Page<Adresses> findAll(Pageable pageable);
    Adresses update(UUID id, Adresses entity);
    void delete(UUID id);
    
    
    
    
    
    
    
    
    
    
}