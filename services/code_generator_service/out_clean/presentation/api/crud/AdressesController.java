package mwm.presentation.controller.crud;

import mwm.domain.entities.Adresses;
import mwm.domain.service.IAdressesCrudService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.validation.annotation.Validated;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import java.util.UUID;
import jakarta.validation.Valid;

@Validated
@RestController
@RequiredArgsConstructor
@RequestMapping("/api/adresses")
public class AdressesController {
    
    private final IAdressesCrudService service;
    
    @PostMapping
    public ResponseEntity<Adresses> create(@Valid @RequestBody Adresses entity) {
        return ResponseEntity.ok(service.create(entity));
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<Adresses> findById(@PathVariable UUID id) {
        return ResponseEntity.ok(service.findById(id));
    }
    
    @GetMapping
    public ResponseEntity<Page<Adresses>> findAll(Pageable pageable) {
        return ResponseEntity.ok(service.findAll(pageable));
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<Adresses> update(
        @PathVariable UUID id,
        @Valid @RequestBody Adresses entity
    ) {
        return ResponseEntity.ok(service.update(id, entity));
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable UUID id) {
        service.delete(id);
        return ResponseEntity.noContent().build();
    }
    
    
    
    
    
    
    
    
    
    
}