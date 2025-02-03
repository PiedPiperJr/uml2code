package mwm.presentation.controller.crud;

import mwm.domain.entities.Student;
import mwm.domain.service.IStudentCrudService;
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
@RequestMapping("/api/student")
public class StudentController {
    
    private final IStudentCrudService service;
    
    @PostMapping
    public ResponseEntity<Student> create(@Valid @RequestBody Student entity) {
        return ResponseEntity.ok(service.create(entity));
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<Student> findById(@PathVariable UUID id) {
        return ResponseEntity.ok(service.findById(id));
    }
    
    @GetMapping
    public ResponseEntity<Page<Student>> findAll(Pageable pageable) {
        return ResponseEntity.ok(service.findAll(pageable));
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<Student> update(
        @PathVariable UUID id,
        @Valid @RequestBody Student entity
    ) {
        return ResponseEntity.ok(service.update(id, entity));
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable UUID id) {
        service.delete(id);
        return ResponseEntity.noContent().build();
    }
    
    
    
    
    
    
}