package org.enspy.4gi.infrastructure.repositories;

import org.enspy.4gi.domain.entities.Student;
import org.enspy.4gi.domain.repositories.IStudentRepository;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.*;

@Repository
public interface StudentJpaRepository extends JpaRepository< Student, UUID>, IStudentRepository< Student, UUID>
{
    //TODO: Implement the repository logic here base on the AI
}