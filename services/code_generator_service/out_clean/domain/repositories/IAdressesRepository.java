package mwm.domain.repositories;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import java.util.List;
import java.util.Optional;

public interface IAdressesRepository<T, ID> {
    T save(T entity);
    Optional<T> findById(ID id);
    Page<T> findAll(Pageable pageable);
    void deleteById(ID id);
    boolean existsById(ID id);
    
    
    
    
    
    
    
    
    
    
}