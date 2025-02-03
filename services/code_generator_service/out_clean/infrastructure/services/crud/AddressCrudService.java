// Service Implementation Template
package mwm.infrastructure.service.crud;

import mwm.domain.entities.Address;
import mwm.domain.service.crud.IAddressCrudService;
import mwm.infrastructure.repositories.AddressJpaRepository;
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
public class AddressService implements IAddressCrudService {
    
    private final AddressJpaRepository repository;
    
    @Override
    public Address create(Address entity) {
        return repository.save(entity);
    }
    
    @Override
    @Transactional(readOnly = true)
    public Address findById(UUID id) {
        return repository.findById(id)
            .orElseThrow(() -> new EntityNotFoundException("Address not found with id: " + id));
    }
    
    @Override
    @Transactional(readOnly = true)
    public Page<Address> findAll(Pageable pageable) {
        return repository.findAll(pageable);
    }
    
    @Override
    public Address update(UUID id, Address entity) {
        if (!repository.existsById(id)) {
            throw new EntityNotFoundException("Address not found with id: " + id);
        }
        entity.setId(id);
        return repository.save(entity);
    }
    
    @Override
    public void delete(UUID id) {
        if (!repository.existsById(id)) {
            throw new EntityNotFoundException("Address not found with id: " + id);
        }
        repository.deleteById(id);
    }
    
    
    
    
    
    
    
    
    
    
    
    
}