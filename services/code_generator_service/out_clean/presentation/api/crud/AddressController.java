package mwm.presentation.controller.crud;

import mwm.domain.entities.Address;
import mwm.domain.service.IAddressCrudService;
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
@RequestMapping("/api/address")
public class AddressController {
    
    private final IAddressCrudService service;
    
    @PostMapping
    public ResponseEntity<Address> create(@Valid @RequestBody Address entity) {
        return ResponseEntity.ok(service.create(entity));
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<Address> findById(@PathVariable UUID id) {
        return ResponseEntity.ok(service.findById(id));
    }
    
    @GetMapping
    public ResponseEntity<Page<Address>> findAll(Pageable pageable) {
        return ResponseEntity.ok(service.findAll(pageable));
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<Address> update(
        @PathVariable UUID id,
        @Valid @RequestBody Address entity
    ) {
        return ResponseEntity.ok(service.update(id, entity));
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable UUID id) {
        service.delete(id);
        return ResponseEntity.noContent().build();
    }
    
    
    
    
    
    
    
    
    
    
    
    
}