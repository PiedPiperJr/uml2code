package mwm.presentation.controller.crud;

import mwm.domain.entities.Person;
import mwm.domain.service.IPersonCrudService;
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
@RequestMapping("/api/person")
public class PersonController {
    
    private final IPersonCrudService service;
    
    @PostMapping
    public ResponseEntity<Person> create(@Valid @RequestBody Person entity) {
        return ResponseEntity.ok(service.create(entity));
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<Person> findById(@PathVariable UUID id) {
        return ResponseEntity.ok(service.findById(id));
    }
    
    @GetMapping
    public ResponseEntity<Page<Person>> findAll(Pageable pageable) {
        return ResponseEntity.ok(service.findAll(pageable));
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<Person> update(
        @PathVariable UUID id,
        @Valid @RequestBody Person entity
    ) {
        return ResponseEntity.ok(service.update(id, entity));
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable UUID id) {
        service.delete(id);
        return ResponseEntity.noContent().build();
    }
    
    
    
    
    
    
    
    
    
    
}