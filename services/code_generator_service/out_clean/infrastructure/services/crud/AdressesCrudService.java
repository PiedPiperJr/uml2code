// Service Implementation Template
package mwm.infrastructure.service.crud;

import mwm.domain.entities.Adresses;
import mwm.domain.service.crud.IAdressesCrudService;
import mwm.infrastructure.repositories.AdressesJpaRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import jakarta.persistence.EntityNotFoundException;
import java.util.UUID;
import java.util.List;

@Service
@RequiredArgsConstructor
@Transactional
public class AdressesService implements IAdressesCrudService {
    
    private final AdressesJpaRepository repository;
    
    @Override
    public Adresses create(Adresses entity) {
        return repository.save(entity);
    }
    
    @Override
    @Transactional(readOnly = true)
    public Adresses findById(UUID id) {
        return repository.findById(id)
            .orElseThrow(() -> new EntityNotFoundException("Adresses not found with id: " + id));
    }
    
    @Override
    @Transactional(readOnly = true)
    public Page<Adresses> findAll(Pageable pageable) {
        return repository.findAll(pageable);
    }
    
    @Override
    public Adresses update(UUID id, Adresses entity) {
        if (!repository.existsById(id)) {
            throw new EntityNotFoundException("Adresses not found with id: " + id);
        }
        entity.setId(id);
        return repository.save(entity);
    }
    
    @Override
    public void delete(UUID id) {
        if (!repository.existsById(id)) {
            throw new EntityNotFoundException("Adresses not found with id: " + id);
        }
        repository.deleteById(id);
    }
    
    
    
    
    
    
    
    
    
    
}